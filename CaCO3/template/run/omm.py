import sys
from mdtraj.reporters import DCDReporter

import openmm
import openmmplumed
from openmm import app
from openmm import unit
from openmmtools import integrators
import os

pdb_file = '../../data/r.pdb'

pdb = app.PDBFile(pdb_file)
forcefield = app.ForceField('../../data/XCO3.xml')
system = forcefield.createSystem(
    pdb.topology,
    nonbondedMethod=app.PME,
    ewaldErrorTolerance=1e-05,
    nonbondedCutoff=0.9 * unit.nanometer,
    useDispersionCorrection=False,
    constraints=None,
    rigidWater=False,
)
for n, f in enumerate(system.getForces()):
    f.setForceGroup(n + 1)

with open('plumed.inp', 'r') as fp:
    plumed = openmmplumed.PlumedForce(fp.read())
system.addForce(plumed)

integrator = integrators.BAOABIntegrator(
    temperature=300 * unit.kelvin,
    collision_rate=1 / unit.picosecond,
    timestep=0.001 * unit.picoseconds
)

platform = openmm.Platform.getPlatformByName('CUDA')
properties = {'DeviceIndex': '0', 'Precision': 'mixed'}
simulation = app.Simulation(
    pdb.topology, system, integrator, platform, properties
)

simulation.context.setPositions(pdb.positions)
simulation.context.setVelocitiesToTemperature(300)
dcd_reporter = DCDReporter('traj.dcd', reportInterval=1000)
screen_reporter = app.StateDataReporter(
    sys.stdout, 1000, step=True, potentialEnergy=True, temperature=True
)
simulation.reporters.append(dcd_reporter)
simulation.reporters.append(screen_reporter)


if os.path.exists('restart.chk'):
    simulation.loadCheckpoint('restart.chk')

simulation.step(30000000)
#simulationlation.runForClockTime(86300 * unit.second, checkpointFile='restart.chk')

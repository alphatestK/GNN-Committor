import sys
from mdtraj.reporters import DCDReporter

import openmm
import openmmplumed
from openmm import app
from openmm import unit
from openmmtools import integrators


pdb_file = '../../data/r.pdb'

pdb = app.PDBFile(pdb_file)
forcefield = app.ForceField('../../data/tip3p_standard.xml')
system = forcefield.createSystem(
    pdb.topology,
    nonbondedMethod=app.PME,
    nonbondedCutoff=0.9*unit.nanometer,
    constraints=app.HBonds
)
with open('plumed.inp', 'r') as fp:
    plumed = openmmplumed.PlumedForce(fp.read())
system.addForce(plumed)

integrator = integrators.GeodesicBAOABIntegrator(
    K_r=4,
    temperature=300 * unit.kelvin,
    collision_rate=1 / unit.picosecond,
    timestep=0.002 * unit.picoseconds
)

platform = openmm.Platform.getPlatformByName('CUDA')
properties = {'DeviceIndex': '0', 'Precision': 'mixed'}
simulation = app.Simulation(
    pdb.topology, system, integrator, platform, properties
)

simulation.context.setPositions(pdb.positions)
dcd_reporter = DCDReporter('traj.dcd', reportInterval=250)
screen_reporter = app.StateDataReporter(
    sys.stdout, 50000, step=True, potentialEnergy=True, temperature=True
)
simulation.reporters.append(dcd_reporter)
simulation.reporters.append(screen_reporter)

simulation.runForClockTime(86300 * unit.second, checkpointFile='restart.chk')
#simulation.step(int(15000000))
#simulation.step(int(5E7))

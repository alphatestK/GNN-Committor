# GNN Committor

This repository contains all the input files and data related to the paper "Committors without Descriptors"

The following folders contains the simulation setup and models for the different systems presented in the manuscript.
```
.
├── Ala2
├── NaCl
├── CaCO3
└── Calixarene
```
And the plugin folder contains the cpp patch for the bias interface in plumed.

The definition and training of GNN committor model is available through the [mlcolvar](https://github.com/luigibonati/mlcolvar/) library. A simple tutorial on NaCl could be found in [/tutorials/adv_gnn_committor.ipynb](https://github.com/alphatestK/GNN-Committor/blob/main/tutorials/adv_gnn_committor.ipynb)

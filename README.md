# Sp0ter

reconstructing events like [this](http://www.phy.bnl.gov/wire-cell/bee/set/9/event/0/).
## Single Pi0 Topographical Event Reconstruction
This framework is designed to be framework to analyze single pi0 events in the MicroBooNE LArTPC. The pi0 almost exclusively decays into two photons which produce electromagnetic showers in the liquid argon. Using the [Wire-Cell](http://www.phy.bnl.gov/wire-cell/) we are able to produce a large data set of 3D-Charge weighted space points. 

### Code Requirements

Requirements: 

* Root version: 6.05 or greater 
* scipy, numpy, sklearn 
* Cython

Also, you will need MC or data from MicroBooNE (not public) 

### Building the code 

In the top directory there is Cython build script called *setup_code.py*. 

```
python setup_code.py build_ext --inplace
```

### About structure

##### App Directory 

Clustering and merging directories contain functions to deal with 3D clustering and object merging. 

SParams directory contains function calls for metrics of the objects.

TS_Qual directory contains tests to deal with cosmics remove and shower/track separation. 

Selection directory contains the script that governs all process steps. 


##### Run Directory 
This contains scripts for executing the whole chain, producing analysis and selection cuts, and also 3D visualizations


### Extras
Now you are ready to go. Since this is for MicroBooNE and not Public use message me for more details.

grossora.neutrino@gmail.com

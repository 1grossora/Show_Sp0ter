from datetime import datetime
start_Rtime = datetime.now()

#LoadTime
import sys, os
sys.path.insert(0, "../")
import numpy as np

import lib.utility.Geo_Utils.detector as detector
import lib.utility.Utils.mchandle as mh
import lib.utility.Utils.datahandle as dh
import lib.Selection.Reco_Clusters as Er
import lib.Selection.Select_NeutralPion as Es
import lib.Selection.ROI_Cluster as Erc


#####################
# Import for special tests
#####################
import lib.Clustering.protocluster as pc
import lib.utility.Utils.labelhanle as lh
import lib.Selection.Ana_Clusters as Ea
import lib.Merging.merger as mr 
#####################
####################



end_Rtime = datetime.now()
delta_Rt = end_Rtime-start_Rtime
print 'RTIME' ,str(delta_Rt.seconds)+' loadtime'
start_Rtime = datetime.now()

#############################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# About this script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#  This script will look at
#  reconsturction of showers assuming 
# we are past the ROI stage useing a lower q
#############################################
#Global Calls
debug = True
#make_jsons = False
make_jsons = True
make_ana = True 
#make_ana = False 
#Charge_thresh = 0.0 
#Charge_thresh = 500 
Charge_thresh = 1000 
method_name = 'test_kd_cosmic'
drun_dir = method_name
jcount = -1


#######################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################

for f in sys.argv[1:]:
    jcount +=1

    # This is for checking process time for things
    start = datetime.now()

    ########################
    # Check if the File is good
    ########################
    ####
    file_info = dh.F_Info_Cosmic(f)
    #file_info = dh.F_Info(f)

    end_Rtime = datetime.now()
    delta_Rt = end_Rtime-start_Rtime
    print 'RTIME' ,str(delta_Rt.seconds)+' comsmicinfo'
    start_Rtime = datetime.now()
    event_start_Rtime = datetime.now()
    ########################
    # File info
    ########################
    if debug:
        print 'Current Event -->  Event Run SubRun : ',file_info[1]

    ########################
    # Is this a Signal Event  AKA One neutron induced pi0
    ########################
    SigEVT =  mh.mc_neutron_induced_contained(f)

    if not SigEVT:
        print 'This is not signal'
        continue
    print 'This a signal'

    end_Rtime = datetime.now()
    delta_Rt = end_Rtime-start_Rtime
    print 'RTIME' ,str(delta_Rt.seconds)+' neutroninducedinfo'
    start_Rtime = datetime.now()

    ########################
    # mc_datalabel info
    # Call this once and get the mc info for the jsons for later
    ########################
    mc_dl =  mh.mc_Obj_points(mh.mc_neutron_induced_OBJ(f))

    ########################
    # make the data dir for json 
    ########################
    jdir = os.getcwd() + '/Bjson/'+drun_dir+ '/'+str(jcount)   # This still is global and can be used later
    if make_jsons:
        if not os.path.isdir(jdir):
            print 'NO DIR.... making one for you'
            os.makedirs(jdir)



    ###

    
    ########################
    # Bring in the MC info 
    ########################
    mcinfo = mh.gamma_mc_info(f)
    mcqdep = mh.gamma_mc_dep(f)
    print mcinfo 
    print mcqdep 


    ########################
    #Bring in  Dataset 
    ########################
    dataset = dh.ConvertWC_InTPC_thresh('{}'.format(f),Charge_thresh)
    print 'size of dataset : ' , str(len(dataset))
    if len(dataset)==0:
        continue
    
    

    ########################
    # Build the reco testing here 
    ########################
    labels = []
    

    labels = pc.kdtree_radius(dataset)
    datasetidx_holder = lh.label_to_idxholder(labels,20) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  

    print 'out of the tree for good'
    # Make a json to view
    if make_jsons:
        dh.MakeJson_Objects(dataset,datasetidx_holder,labels,jdir,jcount,'kd_tree', mc_dl)

    print ' AT THE END'





    #if len(dataset)>=15000 or len(dataset)==0:
        #labels = pc.walker(dataset,6,20) # Runs clustering and returns labels list 
    #else:
        #labels = pc.crawlernn(dataset, 6, 20 ) # Runs clustering and returns labels list 


    #datasetidx_holder = lh.label_to_idxholder(labels,20) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  

    # Bring the merging. 
    #datasetidx_holder , labels = mr.wpca_merge(dataset,labels,datasetidx_holder,.3,50)
    #labels = mr.wpca_merge(dataset,labels,datasetidx_holder,.35,150)

    #datasetidx_holder = lh.label_to_idxholder(labels,20) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  

    #Ea.Ana_Object_photons(dataset, datasetidx_holder, jcount,mcinfo,mcqdep, filename = 'test_photon_ana_obj')



    '''
    ########################
    # mc_datalabel info
    # Call this once and get the mc info for the jsons for later
    ########################
    #mc_dl =  mh.mc_Obj_points(mh.mc_neutron_induced_OBJ(f))

    ########################
    # if the file is bad then continue and fill 
    ########################
    if not file_info[0]:
        continue

    ########################
    # make the data dir for json 
    ########################
    jdir = os.getcwd() + '/Bjson/'+drun_dir+ '/'+str(jcount)   # This still is global and can be used later
    if make_jsons:
        if not os.path.isdir(jdir):
            print 'NO DIR.... making one for you'
            os.makedirs(jdir)

    ########################
    # Print out all the MC Spacepts 
    # Print out all the WC-Reco Spacepts 
    ########################
    if make_jsons:
        dh.MakeJsonMC(f,jdir,jcount,'AlgMC',mc_dl)

    if make_jsons:
        dh.MakeJsonReco(f,jdir,jcount,'AlgSPT',mc_dl)

    ########################
    #Bring in  Dataset 
    ########################
    dataset = dh.ConvertWC_InTPC_thresh('{}'.format(f),Charge_thresh)

    #continue
#######################################################################################

    #####################################################################
    #####################################################################
    ###########  Make the reconsutcion section here   ###################
    #####################################################################
    #####################################################################
    # Input will be dataset.... output will be selected pi0 clusters
    trackidx_holder , showeridx_holder , labels =Er.Reco_trackshower(dataset,mc_dl,jdir,jcount,make_jsons)

    #####################################################################

#######################################################################################
    #####################################################################
    #####################################################################
    ###########  Recluster some of the showers     ######################
    #####################################################################
    #####################################################################


    #print ' length of shower holder before ' , str( len(showeridx_holder))
    showeridx_holder , labels =Er.Reco_showerReCluster(dataset,showeridx_holder,labels,mc_dl,jdir,jcount,make_jsons)
    #print ' length of shower holder after ' , str( len(showeridx_holder))

 
#######################################################################################

    #####################################################################
    #####################################################################
    ###########  Make the selection section here   ######################
    #####################################################################
    #####################################################################

    # Input will be clusters .... output will be matched pairs
    #selidx_holder = Es.CorrelatedObjects(dataset, showeridx_holder,labels)
    #if make_jsons:
    #    dh.MakeJson_Objects(dataset,selidx_holder,labels,jdir,jcount,'SELshower', mc_dl)

    #####################################################################
    #####################################################################

#######################################################################################

    #####################################################################
    #####################################################################
    ###########  Make the ana output here    ############################
    #####################################################################
    #####################################################################

    # This is ana
    if make_ana:
        #Ea.Ana_CutPi0_mc_pair_vtx(f,Charge_thresh,dataset,  jcount, selidx_holder, trackidx_holder,mc_dl, filename='Full_Ana_SelectedPi0_pair')
        Ea.Ana_Pi0_mc_pair_vtx(f,Charge_thresh,dataset,  jcount, showeridx_holder, trackidx_holder,mc_dl, filename='lPi0_pair')
        Ea.Pi0_Ana_Object(f, Charge_thresh,dataset, showeridx_holder, trackidx_holder, jcount, mc_dl,ts='shower', filename='lhullShower_pi0')
        Ea.Pi0_Ana_Object(f, Charge_thresh,dataset, showeridx_holder, trackidx_holder, jcount, mc_dl,ts='track', filename='lhullTrack_pi0')
        #Ea.Ana_CutPi0_mc_pair_vtx(f,Charge_thresh,dataset,  jcount, showeridx_holder, trackidx_holder,mc_dl, filename='WTEST_Ana_SelectedPi0_pair')
        #Ea.Pi0_Ana_Object(f, Charge_thresh,dataset, showeridx_holder, trackidx_holder, jcount, mc_dl,ts='shower', filename='WTEST_Ana_Shower_pi0')
        #Ea.Pi0_Ana_Object(f, Charge_thresh,dataset, showeridx_holder, trackidx_holder, jcount, mc_dl,ts='track', filename='WTEST_Ana_Track_pi0')

#######################################################################################

    end = datetime.now()
    delta = end-start
    print 'time for an event :'
    print delta.seconds
    #time_h.append(delta.seconds)
    continue

    '''

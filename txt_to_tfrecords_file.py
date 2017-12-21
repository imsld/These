import pandas
import numpy
import time
from builtins import str
from _operator import index




colnames_rates = ['service_ID', 'slot', 'rate']
datatype_rates = {'service_ID': numpy.float,
                  'slot': int,
                  'rate': numpy.float}

colnames_new_rates = ['service_ID', 'rate']
datatype_new_rates = {'service_ID': numpy.float,
                      'rate': numpy.float}


colnames_user = ['User ID', 'IP Address', 'Country', 'IP No.', 'AS', 'Latitude', 'Longitude']
datatype_user = {'User ID': numpy.float,
                 'IP Address' :str,
                 'Country':str,
                 'IP No.':str,
                 'AS':str,
                 'Latitude': numpy.float,
                 'Longitude': numpy.float}

colnames_service = ['service_ID', 'WSDL Address', 'Service Provider', 'IP Address', 'Country', 'IP No.',
                    'AS', 'Latitude', 'Longitude']
datatype_service = {'service_ID': numpy.float,
                 'WSDL Address' :str,
                 'Service Provider':str,
                 'IP Address':str,
                 'Country':str,
                 'IP No.':str,
                 'AS' :str,
                 'Latitude': numpy.float,
                 'Longitude': numpy.float}




#*****************************************************#
            # get DataFram of user list#
#*****************************************************# 
def getUserList():
    df = pandas.read_csv('./dataset1/_new_userlist.txt',
                    sep='\t',
                    names=colnames_user,
                    header=None, dtype=datatype_user)
    return df, len(df.index)

#*********************************************************************#
            # get DataFram of ws list#
#*********************************************************************#
def getServiceList():
    df = pandas.read_csv('./dataset1/_new_wslist.txt',
                    sep='\t',
                    names=colnames_service,
                    header=None, dtype=datatype_service)

    return df, len(df.index)

#*********************************************************************#
            # get DataFram of rates at slot time for all user service #
#*********************************************************************#
def get_df_rate_atslot(num_user, df_serviceID_, slot):
    
    df_serviceID = df_serviceID_.set_index("service_ID")
    df_serviceID['rate'] = -1.

    def getFilePath(i):
        if i < 10 : 
            file_name = "user_00" + str(i) + ".txt"  
        elif i < 100 : 
            file_name = "user_0" + str(i) + ".txt"
        else:  
            file_name = "user_" + str(i) + ".txt"
        return "./_userRtData/" + file_name

    
    rt_Matrix = pandas.DataFrame()
    print(rt_Matrix)
    for i in range(num_user):
        # get rtdata file 
        file_path = getFilePath(i);
        df_rtdata = pandas.read_csv(file_path,
                             sep=' ',
                             names=colnames_rates,
                             header=None, dtype=datatype_rates)
        print(file_path)
       
        df_rtdata = df_rtdata[df_rtdata.slot == slot]
        df_filtered = df_rtdata[['service_ID', 'rate']]
        df_filtered = df_filtered.set_index("service_ID")
        df_filtered = df_filtered.append(df_serviceID)        
        df_filtered = df_filtered[~df_filtered.index.duplicated(keep='first')]
        df_filtered = df_filtered.reset_index() 
        df_filtered = df_filtered.sort_values(by='service_ID')
        df_filtered = df_filtered.set_index("service_ID")
        rt_Matrix = pandas.concat([rt_Matrix, df_filtered], axis=1) 
        
    rt_Matrix = rt_Matrix.T
    rt_Matrix.to_csv('./rt_matrices/Matrix_slot_'+str(slot)+'.csv', 
                     sep='\t', 
                     encoding="utf-8", 
                     header=False, 
                     index=False, 
                     float_format='%.3f')
    
         
    
#*********************************************************************#

#*********************************************************************#
def main():
    
    
    df_user, num_user = getUserList()
    df_ws, num_ws = getServiceList()
    df_serviceID = df_ws[['service_ID']]
    print(num_ws)
    num_slot = 64
    for slot in range(num_slot):
        print("slot : "+str(slot))
        get_df_rate_atslot(num_user, df_serviceID[['service_ID']], slot)
     
    
    interval = time.time() - start_time  
    print ("Total time in seconds:", interval)
    
    start_time = time.time()   
    
    
    interval = time.time() - start_time  
    print ("Total time in seconds:", interval)

if __name__ == '__main__':
    start_time = time.time()
    main()
    interval = time.time() - start_time  
    print ("Total time in seconds:", interval)

from SPARQLWrapper import SPARQLWrapper, JSON, XML
import os
import glob
import xml.etree.ElementTree as ET
import xmltodict
import time
from statistics import mean
import platform
import psutil
import cpuinfo


# Provide the directory path
# directory_path_queries_sy = 'queries/syntetic/'
# directory_path_queries_nt = 'queries/micro/nontopological/'
# directory_path_queries_ss = 'queries/micro/spatialselections/'
# directory_path_queries_sj = 'queries/micro/spatialjoins/'
# directory_path_queries_a = 'queries/micro/aggregations/'
# directory_path_queries_gc = 'queries/macro/geocoding/'
# directory_path_queries_rg = 'queries/macro/reversegeocoding/'
# directory_path_queries_ms = 'queries/macro/mapsearch/'
# directory_path_queries_rm = 'queries/macro/rapidmapping/'
# directory_path_queries_cs = 'queries/macro/computestatistics/'

directory_path_queries_sy = 'queries-testable/syntetic/'
directory_path_queries_nt = 'queries-testable/micro/nontopological/'
directory_path_queries_ss = 'queries-testable/micro/spatialselections/'
directory_path_queries_sj = 'queries-testable/micro/spatialjoins/'
directory_path_queries_a = 'queries-testable/micro/aggregations/'
directory_path_queries_gc = 'queries-testable/macro/geocoding/'
directory_path_queries_rg = 'queries-testable/macro/reversegeocoding/'
directory_path_queries_ms = 'queries-testable/macro/mapsearch/'
directory_path_queries_rm = 'queries-testable/macro/rapidmapping/'
directory_path_queries_cs = 'queries-testable/macro/computestatistics/'


# Set up the SPARQL endpoint URL
# sparql = SPARQLWrapper("http://localhost:3030/geographica/query")
sparql = SPARQLWrapper("https://geosparql.isti.cnr.it/fuseki/seminar-openllet/query")
# sparql = SPARQLWrapper("https://testable.isti.cnr.it/fuseki/seminar-openllet/update")



def get_hardware_info():
    # Basic system info
    system_info = {
        'Platform': platform.system(),
        'Platform Version': platform.version(),
        'Platform Release': platform.release(),
        'Architecture': platform.machine(),
        'Processor': platform.processor(),
        'CPU Info': cpuinfo.get_cpu_info()['brand_raw'],
        'Physical Cores': psutil.cpu_count(logical=False),
        'Total Cores': psutil.cpu_count(logical=True),
        'Max Frequency': psutil.cpu_freq().max,
        'Current Frequency': psutil.cpu_freq().current,
        'Total RAM': f"{round(psutil.virtual_memory().total / (1024.0 ** 3))} GB",
        'Available RAM': f"{round(psutil.virtual_memory().available / (1024.0 ** 3))} GB",
        'Total Disk Space': f"{round(psutil.disk_usage('/').total / (1024.0 ** 3))} GB",
        'Used Disk Space': f"{round(psutil.disk_usage('/').used / (1024.0 ** 3))} GB",
        'Free Disk Space': f"{round(psutil.disk_usage('/').free / (1024.0 ** 3))} GB",
        'GPU Info': None  # Optionally, add GPU info if needed (requires additional library)
    }

    return system_info


def read_files_in_directory(directory):
    file_contents = {}
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                file_contents[filename] = file.read()
    
    return file_contents

def read_answer(directory, filename):
    # Find files matching the partial filename
    matching_files = glob.glob(directory + '*' + filename + '*')
    
    

    # Read the content of the first matching file
    if matching_files:
        file_path = matching_files[0]
        with open(file_path, 'r') as file:
            file_content = file.read()
            # print(file_content)
            return file_content
    else:
        print("No matching files found.")

def check_query_result(result, answer):
    # Parse the XML responses
    root_1 = ET.fromstring(result)
    root_2 = ET.fromstring(answer)
    result_1 = xmltodict.parse(result)
    result_2 = xmltodict.parse(answer)
    xka=result_1["sparql"]["results"]["result"]
    xkb=result_2["sparql"]["results"]["result"]
    # print(f"Result1: {xka}")
    # print(f"Result2: {xkb}")
    xxxx = []
    for xka_x in xka:
        xxxx.append(xka_x)
        
    yyyy = []
    for xkb_x in xkb:
        yyyy.append(xkb_x)

    # Compare the results
    if xxxx == yyyy:
        print("The results are the same.")
        return True
    else:
        print("The results are different.")
        # print(f"result_1: {result_1}")
        # print(f"XXXX: {xxxx}")
        # print(f"YYYY: {yyyy}")
        return False
    
# Set the SPARQL query string
# query = """

# PREFIX gml: <http://www.opengis.net/ont/gml#>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# SELECT DISTINCT ?f
# WHERE {
#   ?f rdf:type gml:Surface
# }
# ORDER BY ?f

# """

# Print the results
# for result in results["results"]["bindings"]:
#     print(result["equals"]["value"])


def exec_micro(contents, warm=False):
    for filename, query in contents.items():
        # Remove the extension from the filename
        filename_without_extension = os.path.splitext(filename)[0]
        print(f"Filename: {filename_without_extension}")
        
        # print(f"Content: {query}")
        # queryString = "DELETE WHERE { ?s ?p ?o. }" 
        # Set the query type to SELECT and the response format to JSON
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        sparql.setTimeout(3600)
        sparql.method = 'POST'
        
        if(warm):
            # If warm wxecute the SPARQL query twice and retrieve the results
            try:
                start = time.time()
                results = sparql.query().convert()
                end = time.time()
                # print(results)
                last = end - start
                print("\n{:0.2f} s\n".format(last))
                
                start = time.time()
                results = sparql.query().convert()
                end = time.time()
                # print(results)
                last = end - start
                print("\n{:0.2f} s\n".format(last))
                
            except Exception as e: 
                print(e)
        else:
            # else if cold execute the SPARQL query once and retrieve the results
            try:
                start = time.time()
                results = sparql.query().convert()
                end = time.time()
                # print(results)
                last = end - start
                print("\n{:0.2f} s\n".format(last))
                
            except Exception as e: 
                print(e)


def exec_macro(contents):
    start_time = time.time()  # Track start time
    lst = []  # List to store the average execution times of each batch of queries
    stop = 0

    # Loop will run for a maximum of 240 seconds (4 minutes)
    while stop < 3600:
        end_time = time.time()
        stop = end_time - start_time  # Calculate elapsed time
        print(f"Elapsed time: {stop:.2f} seconds")
        
        avg_for = []  # To store execution times for the current batch of queries
        
        # Loop over each query in the contents dictionary
        for filename, query in contents.items():
            # Remove the extension from the filename
            filename_without_extension = os.path.splitext(filename)[0]
            print(f"Filename: {filename_without_extension}")
            
            # Assuming you have already defined and configured the SPARQL instance
            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            sparql.setTimeout(3600)  # Timeout after 1 hour if the query doesn't complete

            # Execute the SPARQL query and retrieve the results
            try:
                start = time.time()  # Start time for this query
                results = sparql.query().convert()  # Execute the query
                end = time.time()  # End time for this query

                last = end - start  # Query execution time
                print(f"Query time: {last:.2f} seconds")
                
                # Append this execution time to the current batch list
                avg_for.append(last)
                
            except Exception as e:
                print(f"Error executing query: {e}")

        # Calculate the average query time for the current batch
        if avg_for:
            avg_for_mean = mean(avg_for)
            lst.append(avg_for_mean)  # Append the batch's average to the main list
            print(f"Batch average query time: {avg_for_mean:.2f} seconds")
        else:
            print("No queries executed in this batch.")

    # Calculate and print the mean execution time of all batches after all queries have run
    if lst:  # Ensure lst is not empty before calculating the mean
        lst_avg = mean(lst)
        print(f"Overall average query time: {lst_avg:.2f} seconds")
    else:
        print("No batches were executed successfully.")


           
info = get_hardware_info()
for key, value in info.items():
    print(f"{key}: {value}")

# Call the function to read files in the directory
nt_contents = read_files_in_directory(directory_path_queries_nt)
ss_contents = read_files_in_directory(directory_path_queries_ss)
sj_contents = read_files_in_directory(directory_path_queries_sj)
a_contents = read_files_in_directory(directory_path_queries_a)
gc_contents = read_files_in_directory(directory_path_queries_gc)
rg_contents = read_files_in_directory(directory_path_queries_rg)
rg_contents = read_files_in_directory(directory_path_queries_rg)
ms_contents = read_files_in_directory(directory_path_queries_ms)
rm_contents = read_files_in_directory(directory_path_queries_rm)
cs_contents = read_files_in_directory(directory_path_queries_cs)
sy_contents = read_files_in_directory(directory_path_queries_sy)

# Display the file contents

# for i in range(3):

# #Execute micro non topological cold
# exec_micro(nt_contents)
# exec_micro(ss_contents)
# exec_micro(sj_contents)
# exec_micro(a_contents)

# exec_macro(gc_contents)
# exec_macro(rg_contents)
# exec_macro(ms_contents)
# exec_macro(rm_contents)
# exec_macro(cs_contents)

exec_micro(sy_contents)



    
# Molan: Molan-API
#
# Author: Progyan Bhattacharya <progyanb@acm.org>
# Copyright 2018 Tech-Mantra, All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

import subprocess
from Util.Extension import extension
from Util.Del import delete
import os

def build(id, source_code, input_data = None):
    # Get file names from utility method
    source_file, binary_file, input_file, output_file, err_file = extension("c")

    # Write source code to file
    try:
        fsource = open(source_file, "w+")
        fsource.write(source_code)
        fsource.close()
    except Exception as e:
        print(e)
        return { "id": id, "error": "Error occured while writing to file" }, 403

    # Write custom input to file
    fin = None
    if input_data:
        try:
            fin = open(input_file, "w+")
            fin.write(input_data)
            fin.seek(0)
        except Exception as e:
            print(e)
            return { "id": id, "error": "Error occured while processing input" }, 403

    # Open file connections to ouput and error
    try:
        fout = open(output_file, "w+")
        ferr = open(err_file, "w+")
    except Exception as e:
        print(e)
        return { "id": id, "error": "Error occured while creating file" }, 403

    # Call subprocess to compile
    ret_val =  subprocess.call(["gcc", source_file, "-o", binary_file, "-lm", "-pedantic", "-fno-asm"], stdin = None, stdout = None, stderr = ferr)

    # Return object initialized to 'None'
    ret_obj = None

    # Compilation Success
    if ret_val == 0:
        try:
            sub = subprocess.run([binary_file], cwd="data", stdin = fin, stdout = fout, stderr = ferr, timeout=2, check=True, shell=False)
            exe_val = sub.returncode

            # Returned Success
            if exe_val == 0:
                fout.seek(0)
                ret_obj = { "id": id, "status": "Success", "input": input_data, "output": fout.read() }

            # Execution Failed
            else:
                ferr.seek(0)
                err = ferr.read().replace(source_file, "prog.c")
                ret_obj = { "id": id, "status": "Runtime Error", "input": input_data, "output": err }

        # Process killed due to Timeout
        except subprocess.TimeoutExpired:
            ret_obj = { "id": id, "status": "Time Limit Exceeded", "input": input_data }

        # Non-zero Exit Code
        except subprocess.CalledProcessError:
            ret_obj = { "id": id, "status": "Runtime Error", "input": input_data, "output": "Non Zero Exit Code" }

        # Any other Exception
        except Exception:
            ret_obj = { "id": id, "status": "Runtime Error", "input": input_data, "output": "Segmentation Fault" }

    # Compilation Failed
    else:
        ferr.seek(0)
        err = ferr.read().replace(source_file, "prog.c")
        ret_obj = { "id": id, "status": "Compile Error", "input": input_data, "output": err }

    # Close file connections
    if (fin != None):
        fin.close()
    if (fout != None):
        fout.close()
    if (ferr != None):
        ferr.close()

    # Delete all files during production
    if delete(source_file, binary_file, input_file, output_file, err_file) == -1:
        print("Error occured while deleting files")

    # Return result
    return ret_obj, 200

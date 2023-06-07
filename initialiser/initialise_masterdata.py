import argparse as ap
import pybis as pb
ap = ap.ArgumentParser()


def try_doing(func: any):
    def wrapper(*args2, **kwargs):
        try:
            return func(*args2, **kwargs)
        except ValueError as e:
            print(f"Error while doing {args2}: {e}")
    return wrapper

#Add argument to connect to openbis
ap.add_argument("-u", "--username", type=str, required=True, help="openbis username")
ap.add_argument("-p", "--password", type=str, required=True, help="openbis password")
ap.add_argument("-s", "--server", type=str, required=True, help="openbis server")

args = ap.parse_args()

ob = pb.Openbis(args.server, allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True, verify_certificates=False)
ob.login(args.username, args.password)


#Create the new space and project
sp = ob.new_space(code="TEST", description="Test space")
try_doing(sp.save)()
pr = ob.new_project(code="TEST", space="TEST", description="Test project")
try_doing(pr.save)()
#Create the experiment
exp = ob.new_collection(code="TEST", project="/TEST/TEST", type="COLLECTION")
try_doing(exp.save)()
#Create the sample type
date_prop = ob.new_property_type(code="MEASUREMENT_DATE", dataType="TIMESTAMP", label="Measurement date", description="Date of the measurement")
try_doing(date_prop.save)()
st = ob.new_sample_type(code="MEASUREMENT", generatedCodePrefix="MEAS")
try_doing(st.save)()
try_doing(st.assign_property)("MEASUREMENT_DATE")
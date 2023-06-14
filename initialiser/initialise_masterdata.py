import argparse as ap
import pybis as pb
ap = ap.ArgumentParser()


def try_doing(func: any):
    def wrapper(*args2, **kwargs):
        try:
            return func(*args2, **kwargs)
        except Exception as e:
            print(f"Error while doing {args2}: {e}")
    return wrapper

#Add argument to connect to openbis
ap.add_argument("-u", "--username", type=str, required=True, help="openbis username")
ap.add_argument("-p", "--password", type=str, required=True, help="openbis password")
ap.add_argument("-s", "--server", type=str, required=True, help="openbis server")
ap.add_argument("--check", action="store_true", help="Check if the metadata exists")

args = ap.parse_args()
print(args)
ob = pb.Openbis(args.server, allow_http_but_do_not_use_this_in_production_and_only_within_safe_networks=True, verify_certificates=False)
ob.login(args.username, args.password)
print(ob.get_spaces())

sp_name = "SURFAC_MICHAL.GORA_AT_EMPA.CH"

if args.check:
    res = ob.get_space(sp_name)
    if res is None:
        raise ValueError(f"Space {sp_name} does not exist")
else:
    #Create the new space and project
    sp = ob.new_space(code=sp_name, description="Test space")
    try_doing(sp.save)()
    pr = ob.new_project(code="ESFA_EXPERIMENTS", space=sp_name, description="ESFA experiments")
    try_doing(pr.save)()
    #Create the experiment
    exp = ob.new_collection(code="ESFA", project=f"/{sp_name}/ESFA_EXPERIMENTS", type="COLLECTION")
    try_doing(exp.save)()
    #Create the sample type
    date_prop = ob.new_property_type(code="START_DATE", dataType="TIMESTAMP", label="Start date", description="Date of the measurement")
    try_doing(date_prop.save)()
    date_prop = ob.new_property_type(code="EXP_DESCRIPTION", dataType="MULTILINE_VARCHAR", label="Experimental description", description="Experimental description")
    try_doing(date_prop.save)()
    st = try_doing(ob.new_sample_type)(code="EXPERIMENTAL_STEP_MILAR", generatedCodePrefix="EXSTEPMILAR")

    try_doing(st.save)()
    if st is None:
        print(ob.get_sample_types())
        st = ob.get_sample_type("EXPERIMENTAL_STEP_MILAR")
        try_doing(st.save)()
    try_doing(st.assign_property)("START_DATE")
    try_doing(st.assign_property)("EXP_DESCRIPTION")
    try_doing(st.assign_property)("$NAME")
    try_doing(st.save)()
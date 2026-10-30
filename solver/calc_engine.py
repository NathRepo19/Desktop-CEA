from dataclasses import replace
from rocketcea.cea_obj import CEA_Obj
from solver.data_class_custom import CalcSet,ChoiceSet



# Define calculation function 
def compute_val(calc: CalcSet, calc_ch:ChoiceSet): 
    """Return calculated results without modifying the supplied inputs.

    Input pressures stay in bar; only local solver arguments use psia.
    """
    calc = replace(calc) # Makes local copy of calc which gets returned by this function if the solver(s) succeed. Else, nothing is returned and the original calc object remains as is

    if (
    "Calc_obj" not in locals() 
    or Calc_obj.oxName != calc.ox 
    or Calc_obj.fuelName != calc.fuel
    ):
        Calc_obj = CEA_Obj(oxName=calc.ox, fuelName=calc.fuel)

    # Calc_obj = CEA_Obj( oxName=calc.ox, fuelName=calc.fuel)
    
    rho_conv = 16.0185
    enthalpy_conv = 2.326 
    temp_conv = 5/9
    cp_conv = 4.1868
    bar_psia = 14.504 
    psia_pa = 6894.76
    chamber_pressure_psia = calc.chamber_pressure * bar_psia # Convert chamber pressure from bar to psia before feeding to function
    ambient_pressure_psia = calc.amb_pressure * bar_psia # Converts from bar to psia before feeding to rocketcea func
    c_star_val = Calc_obj.get_Cstar(Pc=chamber_pressure_psia, MR=calc.of_ratio)
    c_star_val = c_star_val/3.281 # Converts the output from ft/s to m/s 
    c_star_val = round(c_star_val,2)
    calc.cstar = c_star_val

    T_ad = Calc_obj.get_Tcomb(Pc=chamber_pressure_psia, MR=calc.of_ratio)
    T_ad = T_ad * (5/9) # Convert to K from Rankine
    T_ad = round(T_ad,2)
    calc.chamber_temp = T_ad



    if calc_ch.nzzl_ch == 1:
        isp_vac = Calc_obj.get_Isp(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1,frozenAtThroat=calc.flg2)
        isp_vac = round(isp_vac,2)
        calc.vac_isp = isp_vac

        isp_amb = Calc_obj.estimate_Ambient_Isp(Pc=chamber_pressure_psia,MR = calc.of_ratio,eps=calc.area_ratio, Pamb=ambient_pressure_psia, frozen=calc.flg1, frozenAtThroat=calc.flg2)[0]
        isp_amb = round(isp_amb,2)
        calc.isp_amb = isp_amb

        pc_pe_rat = Calc_obj.get_PcOvPe(Pc=chamber_pressure_psia, MR = calc.of_ratio, eps = calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)
        calc.exit_pressure = chamber_pressure_psia/pc_pe_rat # Now the exit pressure is stored in psia
       
        calc.exit_pressure = calc.exit_pressure * 6894.76 # Multiplying to return value in Pa
        calc.exit_pressure = round(calc.exit_pressure,2)
    else: 
        exit_pressure_psia = calc.exit_pressure/psia_pa
        pc_pe_rat = chamber_pressure_psia/exit_pressure_psia
        calc.area_ratio = Calc_obj.get_eps_at_PcOvPe(Pc = chamber_pressure_psia, MR = calc.of_ratio, PcOvPe = pc_pe_rat, frozen = calc.flg1, frozenAtThroat = calc.flg2)
        calc.area_ratio = round(calc.area_ratio,2)

        isp_vac = Calc_obj.get_Isp(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1,frozenAtThroat=calc.flg2)
        isp_vac = round(isp_vac,2)
        calc.vac_isp = isp_vac

        isp_amb = Calc_obj.estimate_Ambient_Isp(Pc=chamber_pressure_psia,MR = calc.of_ratio,eps=calc.area_ratio, Pamb=ambient_pressure_psia, frozen=calc.flg1, frozenAtThroat=calc.flg2)[0]
        isp_amb = round(isp_amb,2)
        calc.isp_amb = isp_amb

    # Calculate chamber properties 
    if calc_ch.chamber_enth_ch == 1:
        calc.H_ch = Calc_obj.get_Chamber_H(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio) # Returns in btu/lb
        calc.H_ch = enthalpy_conv * calc.H_ch
        calc.H_ch = round(calc.H_ch,2)

    if calc_ch.chamber_sp_heat_ch == 1: 
        calc.cp_ch = Calc_obj.get_Chamber_Cp(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1) # Returns btu/lb degR
        calc.cp_ch = cp_conv * calc.cp_ch
        calc.cp_ch = round(calc.cp_ch,2)

    if calc_ch.mol_wt_ch == 1: 
        calc.mol_wt = Calc_obj.get_Chamber_MolWt_gamma(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio)[0]

    if calc_ch.gamma_ch == 1: 
        calc.gamma_ch = Calc_obj.get_Chamber_MolWt_gamma(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio)[1]
        calc.gamma_ch = round(calc.gamma_ch,2)

    if calc_ch.chamber_rho_ch == 1: 
        calc.rho_ch = Calc_obj.get_Chamber_Density(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio) # Returns in pounds per cu. ft.
        calc.rho_ch = calc.rho_ch*rho_conv
        calc.rho_ch = round(calc.rho_ch,2)

    # Calculate throat properties 
    if calc_ch.throat_enth_ch == 1: 
        calc.H_throat =  Calc_obj.get_Enthalpies(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[1] # Returns in btu/lb
        calc.H_throat = calc.H_throat * enthalpy_conv
        calc.H_throat = round(calc.H_throat,2)

    if calc_ch.throat_rho_ch == 1: 
        calc.rho_throat = Calc_obj.get_Densities(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[1] # returns in lbm/cu_ft
        calc.rho_throat = calc.rho_throat * rho_conv
        calc.rho_throat = round(calc.rho_throat,2)

    if calc_ch.gamma_throat == 1: 
        calc.gamma_throat = Calc_obj.get_Throat_MolWt_gamma(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1)[1]
        calc.gamma_throat = round(calc.gamma_throat,2)

    if calc_ch.mol_wt_throat == 1: 
        calc.mol_wt_throat = Calc_obj.get_Throat_MolWt_gamma(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1)[0]
        calc.mol_wt_throat = round(calc.mol_wt_throat,2)

    if calc_ch.throat_sp_heat_ch == 1: 
        calc.cp_throat = Calc_obj.get_HeatCapacities(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[1] # Returns in BTU/lbm degR
        calc.cp_throat = calc.cp_throat * cp_conv
        calc.cp_throat = round(calc.cp_throat,2)

    if calc_ch.T_throat == 1: 
        calc.T_Throat = Calc_obj.get_Temperatures(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[1]
        calc.T_Throat = calc.T_Throat * temp_conv
        calc.T_Throat = round(calc.T_Throat,2)

    # Calculate exit properties 
    if calc_ch.exit_rho_ch == 1:
        calc.exit_rho = Calc_obj.get_Densities(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[2] # returns in lbm/cu_ft
        calc.exit_rho = 16.0185 * calc.exit_rho
        calc.exit_rho = round(calc.exit_rho,4)

    if calc_ch.exit_sp_heat_ch == 1: 
        calc.exit_cp = Calc_obj.get_HeatCapacities(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[2] # Returns in BTU/lbm degR
        calc.exit_cp = 4.1868 * calc.exit_cp
        calc.exit_cp = round(calc.exit_cp,2)

    if calc_ch.mol_wt_exit == 1: 
        calc.exit_mol_wt = Calc_obj.get_exit_MolWt_gamma(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[0]
        calc.exit_mol_wt = round(calc.exit_mol_wt,2)

    if calc_ch.gamma_exit == 1: 
        calc.exit_gamma = Calc_obj.get_exit_MolWt_gamma(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[1]
        calc.exit_gamma = round(calc.exit_gamma,2)

    if calc_ch.exit_enth_ch == 1: 
        calc.exit_H = Calc_obj.get_Enthalpies(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[2] # Returns in btu/lb
        calc.exit_H = 2.326 * calc.exit_H
        calc.exit_H = round(calc.exit_H,2)

    if calc_ch.mach_num_exit == 1: 
        calc.exit_mach = Calc_obj.get_MachNumber(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)
        calc.exit_mach = round(calc.exit_mach,2)

    if calc_ch.T_exit == 1: 
        calc.T_Exit =  Calc_obj.get_Temperatures(Pc=chamber_pressure_psia, MR=calc.of_ratio, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[2]
        calc.T_Exit = (5/9) * calc.T_Exit
        calc.T_Exit = round(calc.T_Exit,2)
    return calc



def mono_prop_compute_val(calc: CalcSet,calc_ch:ChoiceSet):
    """Return monopropellant results without modifying the supplied inputs.

    Input pressures stay in bar; only local solver arguments use psia.
    """
    calc = replace(calc)


    if (
    "Calc_obj" not in locals() 
    or Calc_obj.propName != calc.mono_prop_name
     
    ):
        Calc_obj = CEA_Obj(propName= calc.mono_prop_name)


    bar_psia = 14.504 
    psia_pa = 6894.76
    chamber_pressure_psia = calc.chamber_pressure * bar_psia # Convert from bar (user input) to psia
    ambient_pressure_psia = calc.amb_pressure * bar_psia

    c_star_val = Calc_obj.get_Cstar(Pc=chamber_pressure_psia, MR=calc.of_ratio)
    c_star_val = c_star_val/3.281 # Converts the output from ft/s to m/s 
    c_star_val = round(c_star_val,2)
    calc.cstar = c_star_val

    T_ad = Calc_obj.get_Tcomb(Pc=chamber_pressure_psia, MR=calc.of_ratio)
    T_ad = T_ad * (5/9) # Convert to K from Rankine
    T_ad = round(T_ad,2)
    calc.chamber_temp = T_ad



    if calc_ch.nzzl_ch == 1:
        isp_vac = Calc_obj.get_Isp(Pc=chamber_pressure_psia,  eps=calc.area_ratio, frozen=calc.flg1,frozenAtThroat=calc.flg2)
        isp_vac = round(isp_vac,2)
        calc.vac_isp = isp_vac

        isp_amb = Calc_obj.estimate_Ambient_Isp(Pc=chamber_pressure_psia,eps=calc.area_ratio, Pamb=ambient_pressure_psia, frozen=calc.flg1, frozenAtThroat=calc.flg2)[0]
        isp_amb = round(isp_amb,2)
        calc.isp_amb = isp_amb

        pc_pe_rat = Calc_obj.get_PcOvPe(Pc=chamber_pressure_psia, eps = calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)
        calc.exit_pressure = chamber_pressure_psia/pc_pe_rat
        calc.exit_pressure = calc.exit_pressure *  psia_pa # Convert from psia to Pa to return to user 
        calc.exit_pressure = round(calc.exit_pressure,2)
    else: 
        exit_pressure_psia = calc.exit_pressure/6895 # Converts user input (in Pa) to psia before determi9ning pressure ratio since chamber pressure also in psia now 
        pc_pe_rat = chamber_pressure_psia/exit_pressure_psia
        calc.area_ratio = Calc_obj.get_eps_at_PcOvPe(Pc = chamber_pressure_psia,  PcOvPe = pc_pe_rat, frozen = calc.flg1, frozenAtThroat = calc.flg2)
        calc.area_ratio = round(calc.area_ratio,2)

        isp_vac = Calc_obj.get_Isp(Pc=chamber_pressure_psia, eps=calc.area_ratio, frozen=calc.flg1,frozenAtThroat=calc.flg2)
        isp_vac = round(isp_vac,2)
        calc.vac_isp = isp_vac

        isp_amb = Calc_obj.estimate_Ambient_Isp(Pc=chamber_pressure_psia,eps=calc.area_ratio, Pamb=ambient_pressure_psia, frozen=calc.flg1, frozenAtThroat=calc.flg2)[0]
        isp_amb = round(isp_amb,2)
        calc.isp_amb = isp_amb

    if calc_ch.chamber_enth_ch == 1:
        calc.H_ch = Calc_obj.get_Chamber_H(Pc=chamber_pressure_psia, eps=calc.area_ratio) # Returns in btu/lb
        calc.H_ch = calc.H_ch*2.326 # Converting from btu/lb to KJ/Kg 
        calc.H_ch = round(calc.H_ch,2) 

    if calc_ch.chamber_sp_heat_ch == 1: 
        calc.cp_ch = Calc_obj.get_Chamber_Cp(Pc=chamber_pressure_psia,  eps=calc.area_ratio, frozen=calc.flg1) # Returns btu/lb degR
        calc.cp_ch = calc.cp_ch * 4.1868 # Converting from btu/lb Deg. Rankine to KJ/Kg - k
        calc.cp_ch = round(calc.cp_ch,2)

    if calc_ch.mol_wt_ch == 1: 
        calc.mol_wt = Calc_obj.get_Chamber_MolWt_gamma(Pc=chamber_pressure_psia,  eps=calc.area_ratio)[0]

    if calc_ch.gamma_ch == 1: 
        calc.gamma_ch = Calc_obj.get_Chamber_MolWt_gamma(Pc=chamber_pressure_psia, eps=calc.area_ratio)[1]
        calc.gamma_ch = round(calc.gamma_ch,2)

    if calc_ch.chamber_rho_ch == 1: 
        calc.rho_ch = Calc_obj.get_Chamber_Density(Pc=chamber_pressure_psia, eps=calc.area_ratio) # Returns in pounds per cu. ft.
        calc.rho_ch = calc.rho_ch * 16.0185 # Converts from pounds/cu_ft to kg/m3
        calc.rho_ch = round(calc.rho_ch,2)


    # Calculate throat properties 
    if calc_ch.throat_enth_ch == 1: 
        calc.H_throat =  Calc_obj.get_Enthalpies(Pc=chamber_pressure_psia, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[1] # Returns in btu/lb
        calc.H_throat = 2.326 * calc.H_throat # Converts from btu/lb to KJ/Kg
        calc.H_throat = round(calc.H_throat,2)

    if calc_ch.throat_rho_ch == 1: 
        calc.rho_throat = Calc_obj.get_Densities(Pc=chamber_pressure_psia, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[1] # returns in lbm/cu_ft
        calc.rho_throat = calc.rho_throat* 16.0185 # Converts from lbm/cu_ft to kg/m3
        calc.rho_throat = round(calc.rho_throat,2)

    if calc_ch.gamma_throat == 1: 
        calc.gamma_throat = Calc_obj.get_Throat_MolWt_gamma(Pc=chamber_pressure_psia, eps=calc.area_ratio, frozen=calc.flg1)[1]
        calc.gamma_throat = round(calc.gamma_throat,2)

    if calc_ch.mol_wt_throat == 1: 
        calc.mol_wt_throat = Calc_obj.get_Throat_MolWt_gamma(Pc=chamber_pressure_psia, eps=calc.area_ratio, frozen=calc.flg1)[0]
        calc.mol_wt_throat = round(calc.mol_wt_throat,2)

    if calc_ch.throat_sp_heat_ch == 1: 
        calc.cp_throat = Calc_obj.get_HeatCapacities(Pc=chamber_pressure_psia, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[1] # Returns in BTU/lbm degR
        calc.cp_throat = calc.cp_throat * 4.1868 # Converts from BTU/lbm Deg R to KJ/Kg-K 
        calc.cp_throat = round(calc.cp_throat,2)

    if calc_ch.T_throat == 1: 
        calc.T_Throat = Calc_obj.get_Temperatures(Pc=chamber_pressure_psia, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[1]
        calc.T_Throat = calc.T_Throat * (5/9) # COnvert rankine to K 
        calc.T_Throat = round(calc.T_Throat,2)


    # Calculate exit properties 
    if calc_ch.exit_rho_ch == 1:
        calc.exit_rho = Calc_obj.get_Densities(Pc=chamber_pressure_psia,  eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[2] # returns in lbm/cu_ft
        calc.exit_rho = calc.exit_rho * 16.0185 
        calc.exit_rho = round(calc.exit_rho,4)

    if calc_ch.exit_sp_heat_ch == 1: 
        calc.exit_cp = Calc_obj.get_HeatCapacities(Pc=chamber_pressure_psia,  eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[2] # Returns in BTU/lbm degR
        calc.exit_cp = calc.exit_cp * 4.1868
        calc.exit_cp = round(calc.exit_cp,2)

    if calc_ch.mol_wt_exit == 1: 
        calc.exit_mol_wt = Calc_obj.get_exit_MolWt_gamma(Pc=chamber_pressure_psia, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[0]
        calc.exit_mol_wt = round(calc.exit_mol_wt,2)

    if calc_ch.gamma_exit == 1: 
        calc.exit_gamma = Calc_obj.get_exit_MolWt_gamma(Pc=chamber_pressure_psia, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[1]
        calc.exit_gamma = round(calc.exit_gamma,2)

    if calc_ch.exit_enth_ch == 1: 
        calc.exit_H = Calc_obj.get_Enthalpies(Pc=chamber_pressure_psia,  eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[2] # Returns in btu/lb
        calc.exit_H = calc.exit_H*2.326
        calc.exit_H = round(calc.exit_H,2)

    if calc_ch.mach_num_exit == 1: 
        calc.exit_mach = Calc_obj.get_MachNumber(Pc=chamber_pressure_psia, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)
        calc.exit_mach = round(calc.exit_mach,2)

    if calc_ch.T_exit == 1: 
        calc.T_Exit =  Calc_obj.get_Temperatures(Pc=chamber_pressure_psia, eps=calc.area_ratio, frozen=calc.flg1, frozenAtThroat=calc.flg2)[2]
        calc.T_Exit = calc.T_Exit * (5/9)
        calc.T_Exit = round(calc.T_Exit,2)

    return calc


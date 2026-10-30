




output_list = [
"Chamber Gas Density (Kg/m3)",
"Chamber Specific Heat (constant pressure) KJ/Kg-K", 
"Chamber Enthalpy (KJ/Kg)",
"Chamber Molecular Wt. (gm/mol)",
"Chamber Sp. Heat Ratio gamma",
"Throat Gas Density (Kg/m3)",
"Throat Gas Temperature (K)",
"Throat Specific Heat (constant pressure) KJ/Kg-K",
"Throat Enthalpy (KJ/Kg)",
"Throat Molecular Wt. (gm/mol)",
"Throat Sp. Heat Ratio gamma",
"Exit Gas Density (Kg/m3)",
"Exit Gas Temperature (K)",
"Exit Specific Heat (constant pressure) KJ/Kg-K",
"Exit Enthalpy (KJ/Kg)",
"Exit Molecular Wt. (gm/mol)",
"Exit Sp. Heat Ratio gamma",
"Exit Mach Number"
]

choice_list = [
"chamber_rho_ch",
"chamber_sp_heat_ch",
"chamber_enth_ch",
"mol_wt_ch",
"gamma_ch",
"throat_rho_ch",
"T_throat",
"throat_sp_heat_ch",
"throat_enth_ch",
"mol_wt_throat",
"gamma_throat",
"exit_rho_ch",
"T_exit",
"exit_sp_heat_ch",
"exit_enth_ch",
"mol_wt_exit",
"gamma_exit",
"mach_num_exit"
]

data_variable_list = [
"rho_ch",
"cp_ch",
"H_ch",
"mol_wt",
"gamma_ch",
"rho_throat",
"T_Throat",
"cp_throat",
"H_throat",
"mol_wt_throat",
"gamma_throat",
"exit_rho",
"T_Exit",
"exit_cp",
"exit_H",
"exit_mol_wt",
"exit_gamma",
"exit_mach"
]

# Dictionary mapping to print csv
var_mapping = { 
"chamber_pressure": "Chamber Pressure (bar)",
"of_ratio": "Oxidizer to Fuel Ratio",
"cstar":"Characteristic Velocity (m/s)",
"chamber_temp":"Adiabatic Flame Temperature (K)",
"vac_isp":"Ideal Vacuum Specific Impulse (s)",
"isp_amb":"Ideal Ambient Specific Impulse (s)",
"area_ratio":"Nozzle Supersonic Area Ratio",
"fuel":"Fuel",
"ox":"oxidizer",
"mono_prop_name":"Monopropellant",
"exit_pressure":"Exit Pressure (Pa)",
"amb_pressure": "Ambient Pressure (bar)",
"mol_wt":"Chamber Gas Mol. Wt. (gm/mol)",
"rho_ch":"Chamber Gas Denisty (Kg/m3)",
"cp_ch":"Chamber Gas Specific Heat (const. pressure) (KJ/Kg-K)",
"H_ch":"Chamber Gas Enthalpy (KJ/Kg)",
"gamma_ch":"Chamber Gas Gamma",
"T_Throat":"Throat Gas Temperature (K)",
"H_throat":"Throat Gas Enthalpy (KJ/Kg)",
"rho_throat":"Throat Gas Density (Kg/m3)",
"gamma_throat":"Throat Gas Gamma",
"mol_wt_throat":"Throat Gas Mol. Wt. (gm/mol)",
"cp_throat": "Throat Gas Specific Heat (const. pressure) (KJ/Kg-K)",
"exit_rho":"Nozzle Exit Gas Density (Kg/m3)",
"exit_cp":"Nozzle Exit Gas Specific Heat (const. pressure) (KJ/Kg-K)",
"exit_gamma":"Nozzle Exit Gas Gamma",
"exit_mol_wt":"Nozzle Exit Gas Mol. Wt. (gm/mol)",
"exit_H":"Nozzle Exit Gas Enthalpy (KJ/Kg)",
"exit_mach":"Nozzle Exit Mach Number",
"T_Exit":"Nozle Exit Gas Temperature (K)",
"solver_setting":"Solver Settings-"
}


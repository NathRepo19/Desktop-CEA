from __future__ import annotations  # MUST be line #1 of your filefrom dataclasses import dataclass

from dataclasses import dataclass

@dataclass
class CalcSet: 
    # Reqd. fields
    chamber_pressure: float
    chamber_temp: float
    cstar: float
    vac_isp: float
    
    # Variables containing propellant names
    fuel: str | None = None
    ox: str | None = None
    mono_prop_name: str | None = None

    # Main_Parameters 
    area_ratio: float | None = None
    of_ratio: float | None = None
    exit_pressure: float | None = None
    amb_pressure: float | None = None

    isp_amb: float | None = None
    

    #Chamber conditions
    H_ch: float | None = None # Chamber enthalpy 
    cp_ch: float | None = None # Specific heat at constant pressure in chamber 
    rho_ch: float | None = None # Density in combustion chamber 
    mol_wt: float | None = None
    gamma_ch: float | None = None 

    #Nozzle Throat conditions 
    T_Throat: float | None = None
    H_throat: float | None = None
    cp_throat: float | None = None
    rho_throat: float | None = None
    mol_wt_throat: float | None = None
    gamma_throat: float | None = None

    #Nozzle exit conditions 
    T_Exit: float | None = None
    exit_H: float | None = None
    exit_cp : float | None = None
    exit_rho : float | None = None
    exit_mol_wt: float | None = None
    exit_gamma: float | None = None
    exit_mach: float | None = None

    #User solver choice variables
    flg1: int | None = None
    flg2: int | None = None 
    solver_setting: str | None = None

    # Sweep parameter of
    sweep_of_low: int | None = None
    sweep_of_high: int | None = None
    sweep_of_num: int | None = None

    # Sweep parameter pc
    sweep_pc_low: int | None = None
    sweep_pc_high: int | None = None
    sweep_pc_num: int | None = None

    # Sweep parameter nozzle
    sweep_nz_low: int | None = None
    sweep_nz_high: int | None = None
    sweep_nz_num: int | None = None





@dataclass
class ChoiceSet:
    mol_wt_ch: int = 0 
    gamma_ch: int = 0
    exit_ch: int  = 0
    nzzl_ch: int = 0 
    chamber_enth_ch: int = 0
    chamber_sp_heat_ch: int = 0
    chamber_rho_ch: int = 0
    throat_rho_ch: int = 0
    throat_sp_heat_ch: int = 0
    throat_enth_ch: int = 0
    mol_wt_throat: int = 0
    gamma_throat: int = 0
    exit_rho_ch: int = 0
    exit_sp_heat_ch: int = 0
    exit_enth_ch: int = 0
    mol_wt_exit: int = 0
    gamma_exit: int = 0
    mach_num_exit: int = 0
    user_extra_outputs: int = 0
    T_throat: int = 0
    T_exit: int = 0

    of_sweep_ch: int = 0 
    pc_sweep_ch: int = 0
    nz_sweep_ch: int = 0 




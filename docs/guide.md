# <img src="../icon.png" alt="Desktop CEA icon" width="30"> User Guide

This guide explains how to use Desktop CEA. It will be updated as the application changes. Please feel free to report bugs or glitches.

## Getting Started

- Download the Windows executable (`.exe`) for Desktop CEA.
- Keep the executable in a dedicated folder to make the application and its output files easier to find. Exports are saved in a `Results (Desktop_CEA)` subfolder of the application's working directory.
- Double-click the executable to launch the application.

Click any screenshot below to view it at full size. Small screenshots are displayed at their original pixel width to keep interface text sharp.

## Running a Basic Calculation

### 1. Launch the application

Choose the **Monopropellant** or **Bipropellant** tab. The example below uses the **Bipropellant** tab.

<a href="../Images/screenshot_2_opening_new.png">
  <img src="../Images/screenshot_2_opening_new.png"
      alt="Desktop CEA opening screen"
      width="360">
</a>

*The main window, ready for your inputs*

### 2. Choose your propellant(s)

Select an oxidizer and fuel from the drop-down menus for a bipropellant calculation, or a single propellant for a monopropellant calculation.

<a href="../Images/screenshot_4_select_prop_new.png">
  <img src="../Images/screenshot_4_select_prop_new.png"
      alt="Select Propellant Screen"
      width="356">
</a>

*Drop-down menu showing different fuel options*

### 3. Enter input conditions

Enter the O/F (oxidizer-to-fuel mass) ratio for a bipropellant calculation, chamber pressure, and ambient pressure. Chamber and ambient pressures are entered in **bar**. Choose either a nozzle area ratio or a nozzle exit pressure in **Pa**.

To reproduce the basic calculation below, select **90_H2O2** and **Kerosene**, then enter an **O/F ratio of 2.50**, **chamber pressure of 20 bar**, **ambient pressure of 1 bar**, and **nozzle area ratio of 40**. Keep **Equilibrium upto exit** selected.

<a href="../Images/screenshot_5_inputs.png">
  <img src="../Images/screenshot_5_inputs.png"
      alt="Enter input conditions"
      width="353">
</a>

*Enter input conditions in the corresponding boxes and choose exit conditions (nozzle area ratio or exit pressure)*

### 4. Calculate the results

Click **Calculate**. The results will appear below the button.

<a href="../Images/screenshot_3_basic_calc_new.png">
  <img src="../Images/screenshot_3_basic_calc_new.png"
      alt="Simple Calculation Results"
      width="356">
</a>

*Results for hydrogen peroxide (90% concentration) and kerosene*

### 5. Save results

Click **Export Results to CSV** and enter a filename without the `.csv` extension; the application adds it automatically. Results are saved in the `Results (Desktop_CEA)` subfolder of the application's working directory.

<a href="../Images/screenshot_3_csv_basic.png">
  <img src="../Images/screenshot_3_csv_basic.png"
      alt="Simple Calculation Results as shown in CSV format"
      width="466">
</a>

*Saved CSV results opened in Microsoft Excel*

**Note:** Each export contains the most recent calculation. Export a result before running another calculation if you want to keep it. Use a different filename for each export to avoid overwriting an existing file.

## Additional Features

### 1. Select solver mode

Choose a solver mode above the **Select Additional Outputs** button.

<a href="../Images/screenshot_6_solver_settings.png">
  <img src="../Images/screenshot_6_solver_settings.png"
       alt="Solver mode options in the main window"
       width="354">
</a>

*Choose equilibrium expansion or freeze the gas composition at the throat or chamber.*

- **Equilibrium upto exit:** Assumes chemical equilibrium throughout the chamber, nozzle throat, and nozzle exit.
- **Frozen at Throat:** Uses equilibrium composition up to the throat, then holds that composition fixed during expansion to the exit.
- **Frozen at Chamber:** Holds the combustion-chamber composition fixed during expansion through the nozzle.

Here, *frozen* refers to chemical composition; temperature and pressure still change during expansion. See the [RocketCEA documentation](https://rocketcea.readthedocs.io/en/stable/std_examples.html#frozen-performance) for more on frozen-composition calculations.

### 2. Select additional outputs

Use **Select Additional Outputs** to choose properties such as chamber enthalpy, throat gas temperature, or exit Mach number. Select the properties you need and click **OK** to open the **Displaying Additional Outputs** dialog.

The selected properties are included when you calculate results and export them with **Export Results to CSV**.

<a href="../Images/screenshot_7_solver_additional_outputs.png">
  <img src="../Images/screenshot_7_solver_additional_outputs.png"
       alt="Additional output selection on the left and the corresponding results dialog on the right"
       width="800">
</a>

*Choose additional outputs (left) and view their calculated values (right).*

### 3. Parameter sweep

A parameter sweep calculates results at evenly spaced points across a range of O/F ratios, chamber pressures, or nozzle area ratios. O/F sweeps are available for bipropellants; chamber-pressure and nozzle-area-ratio sweeps are available for both propellant types.

The example below sweeps the O/F ratio for hydrogen peroxide (90% concentration) and kerosene.

#### a. Set your input conditions

In the **Bipropellant** tab, select the propellants and set these conditions:

- **Chamber pressure:** 10 bar.
- **Ambient pressure:** 1 bar.
- **Nozzle area ratio:** 50 (choose the nozzle-area-ratio input option).
- **Solver mode:** Equilibrium upto exit.

The O/F value in the main window is replaced by the sweep values. Sweeps use the nozzle area ratio rather than a specified exit pressure.

<a href="../Images/screenshot_9_input_sweep.png">
  <img src="../Images/screenshot_9_input_sweep.png"
       alt="Main window inputs for the hydrogen peroxide and kerosene O/F sweep"
       width="347">
</a>

*Set the fixed input conditions before opening the sweep dialog.*

#### b. Open the parameter sweep dialog

Click **Perform Parameter Sweep** at the bottom of the main window.

<a href="../Images/screenshot_8_sweep.png">
  <img src="../Images/screenshot_8_sweep.png"
       alt="Parameter sweep dialog with sweep controls and an empty plot"
       width="720">
</a>

*Choose the parameter you want to sweep.*

#### c. Set the sweep range and compute results

Select **O/F Sweep** and enter:

- **Lower Limit:** 2.
- **Upper Limit:** 10.
- **Number of Points:** 50.

To include extra properties, check **Select Additional Outputs** and choose from the list that appears. For this example, select **Exit Gas Temperature (K)**. Sweep outputs are selected separately from the additional outputs in the main window.

<a href="../Images/screenshot_10_output_sweeps.png">
  <img src="../Images/screenshot_10_output_sweeps.png"
       alt="O/F sweep from 2 to 10 with 50 points and exit gas temperature selected"
       width="800">
</a>

*Set the sweep range and select any additional outputs before computing.*

Click **Compute**. Once the calculation finishes, the results are available to plot or save. If you change the inputs or selected outputs, click **Compute** again to update the results.

#### d. Plot the results

After computing, the **Y-Axis** drop-down lists the default outputs and any additional outputs you selected. The **X-Axis** corresponds to the parameter being swept.

<a href="../Images/screenshot_12_plot_options.png">
  <img src="../Images/screenshot_12_plot_options.png"
       alt="Y-Axis drop-down listing the outputs available for plotting"
       width="360">
</a>

*Choose an output to plot against the O/F ratio.*

Select vacuum specific impulse (**Vaccum Isp (s)** in the drop-down), then click **Plot**.

<a href="../Images/screenshot_11_output_plot.png">
  <img src="../Images/screenshot_11_output_plot.png"
       alt="Vacuum specific impulse plotted against O/F ratio"
       width="800">
</a>

*Vacuum specific impulse (s) as a function of O/F ratio.*

#### e. Find the peak

Click **Find Maxima** to mark and annotate the peak of the selected output. In this example, the highest sampled vacuum specific impulse is **317.26 s** at an **O/F ratio of 8.04**.

<a href="../Images/screenshot_13_peak.png">
  <img src="../Images/screenshot_13_peak.png"
       alt="Plot annotated with a peak vacuum specific impulse of 317.26 seconds at an O/F ratio of 8.04"
       width="800">
</a>

*The peak identified in the computed sweep.*

**Note:** The peak is found from the sampled points; it is not a separate optimization calculation. To refine the O/F estimate, narrow the sweep range around the peak and increase the number of points. A curve that only increases, only decreases, or remains constant will display **Maxima not found**, even though it has a highest sampled value.

#### f. Save the graph and sweep data

- **Save this Graph:** Enter a filename such as `of_sweep.png` to save the current graph as a PNG image.
- **Save to csv:** Enter a filename such as `of_sweep` to save the most recently computed sweep, including additional outputs. The application adds the `.csv` extension if needed.

Both files are saved in the `Results (Desktop_CEA)` subfolder of the application's working directory. Save the graph after plotting and adding any peak annotation you want to keep.

**Note:** Save sweep data before computing another sweep if you want to keep it. Use a different filename for each export to avoid overwriting an existing file.

### 4. Add a custom propellant

Use this feature to define a propellant from its composition and thermodynamic inputs. You will need:

- A propellant name and chemical formula.
- Element symbols and the number of atoms of each element.
- Formation enthalpy in **cal/mol** at the reference temperature.
- Reference temperature in **K** (298.15 K by default).
- Density in **g/cc** (optional).

#### a. Open the custom propellant tab

Click the **Add Custom Propellant** tab in the main window.

#### b. Enter the name, formula, and thermodynamic inputs

For the butane example shown below, enter **butane** as the name, **C4H10** as the chemical formula, **-30186.42 cal/mol** as the formation enthalpy, and **298.00 K** as the reference temperature. Leave density at **0.00 g/cc** to omit this optional input.

#### c. Enter the element symbols and atom counts

Enter **C** and **4** in the first element row. Click **ADD** once to create a second row, then enter **H** and **10**. Element symbols go on the left and atom counts on the right. For other propellants, use **ADD** to create more rows and **DEL** to remove the last row.

<a href="../Images/screenshot_14_butane_new.png">
  <img src="../Images/screenshot_14_butane_new.png"
       alt="Screenshot showing populated input fields for adding butane as a custom fuel"
       width="358">
</a>

*Butane composition and thermodynamic inputs.*

#### d. Add the propellant

Click **Add as fuel** to add butane to the fuel drop-down in the **Bipropellant** tab. To register a custom oxidizer or monopropellant instead, use **Add as Oxidizer** or **Add as Monopropellant**.

#### e. Use your new propellant

Return to the **Bipropellant** tab. The new fuel, **butane**, appears at the end of the fuel drop-down.

<a href="../Images/screenshot_15_butane_added_new.png">
  <img src="../Images/screenshot_15_butane_added_new.png"
       alt="Screenshot showing newly-added butane in the drop-down menu within the bipropellant tab"
       width="355">
</a>

*The custom fuel is now available for selection.*

Select **butane** as the fuel and **AIR** as the oxidizer. Set the **O/F ratio to 2.50**, **chamber pressure to 20 bar**, **ambient pressure to 1 bar**, and **nozzle area ratio to 40**. Select **Equilibrium upto exit**, then click **Calculate**.

<a href="../Images/screenshot_16_butane_calc_basic_new.png">
  <img src="../Images/screenshot_16_butane_calc_basic_new.png"
       alt="Screenshot showing calculated values for butane"
       width="358">
</a>

*Calculated results for butane and air at the specified conditions.*

### 5. Add a custom blend

Create a blend from two or more propellants using percentages by mass. The component percentages must add up to **100%**.

#### a. Enter a blend name

Open the **Add Custom Propellant** tab and find the **Create a Propellant Blend** section. Enter **butane_h2** as the blend name. This example uses **90% butane** and **10% gaseous hydrogen** by mass. Add butane as a fuel using the steps above before creating this blend.

#### b. Select the blend type

Choose **Fuel Blend** from **Select Blend Type**. The other options are **Oxidizer Blend** and **Monopropellant Blend**. Select the type before adding components; changing it clears the component rows.

#### c. Add the components and percentages

Click **ADD** twice in the blend section to create two component rows. In the first row, select **butane** and enter **90** in the percentage box on the right. In the second row, select **GH2** (gaseous hydrogen) and enter **10**. Use **DEL** to remove the last component row if needed.

<a href="../Images/screenshot_17_butane_h2_blend_new.png">
  <img src="../Images/screenshot_17_butane_h2_blend_new.png"
       alt="Screenshot showing input values for butane-hydrogen fuel blend"
       width="337">
</a>

*A fuel blend containing 90% butane and 10% gaseous hydrogen by mass.*

#### d. Add the blend

Click **Add blend to database**. The blend is now available as **butane_h2** in the fuel drop-down for the current application session.

#### e. Use your new fuel blend

Return to the **Bipropellant** tab, select **butane_h2** as the fuel and **AIR** as the oxidizer, and keep the same input conditions and solver mode as the butane calculation above. Click **Calculate**.

<a href="../Images/screenshot_18_butane_h2_blend_calc_new.png">
  <img src="../Images/screenshot_18_butane_h2_blend_calc_new.png"
       alt="Screenshot showing calculation results with butane-hydrogen fuel blend"
       width="357">
</a>

*Calculated results for the butane–hydrogen blend and air.*

In the examples shown, vacuum specific impulse increases from **201.81 s** for butane to **220.68 s** for the blend containing 10% gaseous hydrogen by mass. This comparison applies to the specified inputs and solver mode; results will change with composition and calculation settings.

## Current limitations

- The rocket motor is modeled as an infinite-area combustor. A finite-area combustor model with a contraction area ratio input is not available.
- Chemical species concentrations are not available in the interface.
- Custom propellants and blends are stored only for the current application session. Add them again after restarting the application, including any custom components needed for a blend.

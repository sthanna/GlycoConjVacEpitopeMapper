# 🧪 Virtual Lab: Build Your Own Vaccine Design Computer
## A Step-by-Step Guide for Young Scientists

Welcome to the **Virtual Lab**! Today, you are going to set up a supercomputer program that scientists use to design new vaccines. It might look like just typing codes, but you are actually building a digital laboratory that simulates how atoms and molecules move.

---

### 📚 What Are We Building?
Imagine you want to build a puzzle (a vaccine) that connects to a specific piece of a bacteria (the target). If you build it right, your body learns to fight the bacteria. We are using **computer code** to find the perfect spot to connect our vaccine puzzle piece.

### 🛠️ What You Need (Prerequisites)
1.  **A Computer**: Windows, Mac, or Linux.
2.  **Internet Access**: To download the tools.
3.  **Curiosity**: Things might break, and that's okay! Science is about fixing mistakes.

---

### Step 1: Setting Up Your "Lab Bench" (Installation)

Before we do experiments, we need to organize our tools. In computer science, we use something called **Conda**.

**Why do we do this?**
> Think of your computer like a kitchen. You don't want to mix your spicy taco ingredients with your cupcake baking. Conda creates a special "box" (called an environment) where we keep only the tools for this specific science project, so nothing gets mixed up!

**Instructions:**
1.  Download **Miniconda** from the internet and install it.
2.  Open the special window called "Anaconda Prompt" (Windows) or "Terminal" (Mac/Linux).
3.  Type this command to create your box:
    ```bash
    conda create -n virtual_lab python=3.10
    ```
4.  Open the box:
    ```bash
    conda activate virtual_lab
    ```

---

### Step 2: Downloading the Blueprint (Get the Code)

Now we need the instructions to run the lab. We get this from **GitHub**.

**Why do we do this?**
> Programmers share their work in big libraries called "repositories." Cloning a repository is like checking out a book that has all the recipes we need to run our experiments.

**Instructions:**
1.  In your terminal window, type:
    ```bash
    git clone https://github.com/YourUsername/virtual-lab.git
    cd virtual-lab
    ```
    *(Note: Replace the link with the specific link to this project)*

2.  Now install the specific robot helpers we need (like OpenMM):
    ```bash
    conda env update --file environment.yml
    ```
    *This might take a while—grab a snack! The computer is downloading huge math libraries.*

---

### Step 3: Finding the Target (Data Prep)

We are researching a bacteria that causes meningitis. We need a map of its surface protein.

**Why do we do this?**
> If you want to design a key for a lock, you first need to look closely at the lock. In our case, the "lock" is a protein called **MenA**, and we download its 3D shape structure (a PDB file) to study it.

**Instructions:**
1.  We have included a starter shape file in `data/structures/pdb4ae1.pdb`.
2.  This file is a list of thousands of atoms and their 3D coordinates (X, Y, Z positions).

---

### Step 4: Running the Simulation (The Experiment)

This is the coolest part. We are going to use a "Physics Engine" called **OpenMM**.

**Why do we do this?**
> Atoms are always wigging and jiggling. To know if a vaccine will stick, we can't just look at a still picture. We have to simulate the jiggling! We use Newton's Laws of Physics (like $F=ma$) to calculate how every single atom moves thousands of times a second.

**Instructions:**
Run the simulation agent with this command:
```bash
python src/virtual_lab/chemistry/run_amber_simulation.py --real
```

**What is happening?**
1.  **Refining**: The code fixes any broken parts of the 3D model.
2.  **Solvating**: It puts the protein inside a virtual drop of water (because proteins live in water in your body!).
3.  **Simulating**: It calculates the movement. You will see output like `Step 100... Step 200...`. This is the computer "watching" the protein move.

---

### Step 5: Did it Work? (Analysis)

After the simulation finishes, we check the results.

**Why do we do this?**
> A simulation is useless if we don't look at the data. We measure something called **RMSF** (Root Mean Square Fluctuation). That's a fancy way of asking: "How much did this part wiggle?"

**Instructions:**
Run the validation script:
```bash
python validate_trajectory.py
```

**Understanding the Result:**
*   **High Number**: The part wiggled a lot (it's floppy).
*   **Low Number**: The part stayed still (it's stiff).
*   **Zero**: Something went wrong—atoms never stop moving!

---

### 🎓 Congratulations!

You just ran a computational biology experiment! You set up a complex environment, simulated the physics of a real protein, and analyzed the data. This is exactly what real computational biologists do every day to discover new medicines.

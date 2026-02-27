# 🌟 OEMA Calibration Report Number Generator 🌟
### *a tiny utility that prevents technicians from summoning duplicate paperwork*

> “If two calibration reports share the same number…  
> the auditors appear.”  

This script safely generates **sequential calibration report numbers** for the Ohio EMA Radiological Instrument Calibration Lab and records them with a timestamp so every instrument calibration can be traced.

Originally written in **2009** and modernized in **2026**, this tool exists for one simple reason:

Radiation instruments must be documented perfectly.  
Humans are bad at counting past 3 when busy.

The computer is now responsible.

---

## 🧠 What Problem This Solves

Every time a survey meter, dosimeter, or detector is calibrated, a **unique calibration report number** must be issued.  
Historically, these were tracked manually or by shared log files.

Problems that happen without this tool:
- duplicate report numbers
- skipped numbers
- overwritten logs
- “who used the last number???”
- audit findings (the scary kind)

This script becomes the **authoritative counter** for the lab.

It:
✔ remembers the last number  
✔ increments correctly  
✔ timestamps every report  
✔ never overwrites history  
✔ works even after power loss or closing the window

---

## 🧾 What the Program Actually Does

When run, the script:

1. Looks for an existing report history
2. Copies legacy data if needed
3. Finds the most recent calibration report number
4. Waits for a technician to press **Enter**
5. Generates the next report number
6. Writes it to a permanent log with date & time

It continues doing this forever until you type `q`.

On Windows, if standard input is unavailable, the script automatically switches to keyboard mode so **Enter** and `q` still work.

---

## 📂 Files Used

| File | Purpose |
|------|------|
| `repnum.txt` | Legacy historical report log (original system) |
| `repnum2.txt` | Active working report number log (current system) |

The script **never deletes or overwrites history**.

### First Run Behavior
If `repnum2.txt` does not exist:

- If `repnum.txt` exists → it copies it
- If not → it creates a new blank log

This ensures continuity across decades of calibration records.

---

## 🧱 Output Format

Every time a report number is issued, a line is appended:

```

MM-DD-YYYY  HH:MM:SS  ######

```

Timestamp note: the script writes fixed **EST (UTC-5)** time.

Example:
```

02-27-2026  09:14:22    1043
02-27-2026  09:17:08    1044
02-27-2026  09:19:31    1045

```

This creates a legally defensible audit trail:
- when the calibration happened
- in what order
- and that no numbers were reused

---

## 🖥️ Requirements

- Python **2.5.2+** (primary target) or **3.x**
- No external packages
- Runs on:
  - Windows
  - Linux
  - Raspberry Pi (yes, it works perfectly on a lab Pi)

Libraries used:
```

os
shutil
time

```

No installation needed.  
No internet needed.  
No IT ticket needed.

---

## ▶️ Running the Program

Open a terminal in the folder containing the script and run:

```
python repnum2.py
```

On Windows PowerShell (when using Python 2.5 specifically):

```
py -2.5 repnum2.py
```

You will see:

```
Calibration Report Number Generator - Version 2.0

How this works:

* Existing report history is copied from repnum.txt to repnum2.txt once (if needed).
* Press Enter to generate and save the next report number.
* Type q and press Enter to quit, or close the window to exit.

Working log file: .../repnum2.txt
Last saved report number: ####

```

---

## 🎛️ Using the Program

| Action | Result |
|------|------|
| Press **Enter** | Generates next calibration report number |
| Type **q** | Safely exits program |
| Close window | Safe — data already written |

Example:

```
Press Enter for next report number or type q to exit:
The next report number in the sequence is 1046

Press Enter for next report number or type q to exit:
The next report number in the sequence is 1047

Press Enter for next report number or type q to exit: q
Program closed.
```

---

## 🔎 How It Determines the Next Number

The script scans `repnum2.txt` line by line and:

1. Splits each line into words
2. Looks for a numeric third column
3. Uses the LAST valid number found
4. Adds +1

So even if:
- the computer crashes
- power goes out
- someone closes the window

…the next number will still be correct.

If no valid number exists → numbering starts at **1**.

---

## 🔒 Safety Features

- Never overwrites existing records
- Appends only
- Survives reboot
- Handles missing files
- Handles empty files
- Handles corrupted lines (skips them safely)

The only way to lose numbering is to delete `repnum2.txt`.

So don’t do that 🙂

---

## 🧪 Why Two Files?

`repnum.txt`  
= historical archive (read-only legacy)

`repnum2.txt`  
= active working counter

This preserves original records while allowing continued operation.

Think of it like:
> `repnum.txt` = the vault  
> `repnum2.txt` = the checkout log

---

## 🛠️ Troubleshooting

### It started at 1
`repnum2.txt` was missing or contained no valid numbers.

Check:
- correct directory
- file permissions
- formatting

### Numbers look wrong
Open `repnum2.txt` and verify lines look like:

```

02-27-2026  09:14:22    1043

```

If someone edited the file manually and broke spacing, the parser may ignore it.

### Nothing happens when pressing Enter
You probably double-clicked it.  
Run it from a terminal instead.

### It opens and closes immediately
This usually means the script was launched outside an interactive terminal input stream.

Use PowerShell or Command Prompt and run:

```
python repnum2.py
```

If input is still unavailable, the script switches to Windows keyboard mode and continues accepting **Enter** and `q`.

---

## 🧯 Important Operational Rule

This program should be running **whenever calibrations are being performed**.

Treat it like:
- a standard
- a reference instrument
- or the source itself

Because administratively… it is.

---

## 📜 Revision History

| Date | Version | Notes |
|------|------|------|
| Sept 2009 | 1.0 | Original OEMA calibration number generator |
| March 2026 | 2.0 | Python 2.5.2+ support, Python 3 compatibility, fixed EST timestamps, safer file handling |

---

## 👩‍🔬 Authors

K. Herminghuysen  
K. Zakutnyi

Radiological Instrument Calibration Lab  
Ohio Emergency Management Agency

---

## Final Note

This is a very small script.

But during an audit, this tiny script becomes one of the most important systems in the lab — because it proves:

- calibrations happened
- in order
- and were controlled

Which, in radiation work, matters more than almost anything.

Happy calibrating.
Stay ALARA ☢️

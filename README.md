# Uni Hacker

## Installation and Setup

### Cloning the repo

In your terminal navigate to the desired directory and clone:

```bash
git clone git@github.com:aiden-d/uni_hacker.git
```

### Setting up env

Navigate into the repo

```bash
cd uni_hacker
```

Create a .env file for the regular expressions

```bash
touch .env
```

Edit the file

```
nano .env
```

Put any desired regular expressions for matching the questions and solutions, each followed by a semi-colon. Otherwise just copy and pase these standard ones:

```
EXPRS="^[ ]*[*]+[ ]*[0-9]+[.][ ]*([\\][n]|[\n]);^[ ]*([Q]|[S])+[ ]*[0-9]+[.][ ]*([\\][n]|[\n])"
```

Save and exit the file

### Installing dependencies

Install dependencies using pip:

```bash
pip3 install fitz re genanki dotenv
```

## Running the code

It may be simpler to copy and paste the relevant pdf files (questions and solutions) into the root directory of the project.

Then they can simply be references as `q1.pdf` and `s1.pdf` for example.

From the root directory of the project run the code:

``` bash
python3 ankiproblems.py
```

And input the relevant data.

The program will generate a series of images, which will be cleaned up before termination.

Once done you should receive an Anki file. Assuming you have Anki installed, double click it in your file explorer and import. 
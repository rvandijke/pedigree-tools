# Pedigree Tools

This python package can read CSV pedigree files and derive missing year or births based on a set of rules.

The default "Derive YOBs" operation derives years of birth for individuals where diag* fields have a value other than "0".
The "calculate all derive YOBs" operation ignores the diag fields and calculates all YOBs.

# Installation

Install with pip:

`pip install git+https://github.com/rvandijke/pedigree-tools.git`

# Launching

Launch `pedigree-tools` to start the script.

## Rules

The following rules are applied (in this order):

1) By siblings: If yob of siblings is known (same MothID), take the average of siblings
2) By mother: If yob mother is known, that yob mother + 25
3) By oldest child: If yob childs are known, that the oldest - 25
4) By father: If yob father is known, take yob father + 25
5) By grandparents: If yob grandparents are known, take that yob + 50 (try mother first)
6) By oldest grand child: If yob grandchildren are known, take the oldest - 50
7) By cousins: if yob or cousins are known, take the average
8) By generations: Go to the complete upper generation, see if average is known. Otherwise go to lower generation and see if average is known. Go through generation layers until a yob is derived.

## File Format

- Supported file format is CSV only
- Column headers must match: `FID,Target,IndivID,FathID,MothID,Sex 1=m / 2=v,Twin,Dead,Age,Yob,diag1,diag2,diag3,diag4,diag5`
  - Specify as many diag* fields as required

## No tests / no warranty

This software is provided as is and it's output is not guaranteed to be correct. No tests are provided with this software and use of it is at your own risk. 

## No active development

This package is not actively maintained and is put online for demonstration purposes


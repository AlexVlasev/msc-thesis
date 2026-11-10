# MSc Thesis Archive

When I worked on my thesis[^vlasev] all the way back in 2014 and 2015 I didn't use Git. Instead, I made copies of the whole thesis project and used those as my version control. I've always wanted to replay that history, so to speak, as if I had used Git. This repository is exactly that.

The `replay.py` script takes the first snapshot in chronological order and replaces the contents of `thesis/` with the contents of the snapshot. Then it moves the snapshot to the `processed/` folder. It also determines what the commit datetime should be and it adds the files to Git. Finally it prints a command that lets me craft a commit message and commit the results.

On 2026-11-10, I went through the collection of thesis snapshots using the `replay.py` script. I crafted each commit message based on the diffs between runs. After

I crafted each one based on the diffs between runs. Each Git commit was made on 2026-11-10 but backdated to the newest datetime of any of the tracked files of a given thesis snapshot. After 64 commits, the archive was completed.

[^vlasev]: Vlasev, A. (2015). Multidimensional lattice walk enumeration through coefficient extraction operators (T). University of British Columbia. [UBC Open Library](https://open.library.ubc.ca/collections/ubctheses/24/items/1.0165809) / [DOI:10.14288/1.0165809](https://dx.doi.org/10.14288/1.0165809)

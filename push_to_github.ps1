
# Assuming we are already in the repo from previous run

# Configure Remote (Duplicate safe)
git remote remove origin 2>$null
git remote add origin https://github.com/sthanna/GlycoConjVacEpitopeMapper.git

# Fetch remote
git fetch origin

# Merge remote changes into local main
# -X ours: If conflict (e.g. README), keep LOCAL version
# --allow-unrelated-histories: if repo was created with README/LICENSE
git merge origin/main --allow-unrelated-histories -X ours -m "Merge remote to sync histories"

# Push to main
git push -u origin main

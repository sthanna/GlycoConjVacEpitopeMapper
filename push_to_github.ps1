
# Initialize or Re-initialize Git
if (-not (Test-Path .git)) {
    git init
}

# Add all files
git add .

# Commit
git commit -m "Initial commit for GlycoConjVacEpitopeMapper: Agents, RAG, and Real Data Pipeline"

# Rename branch to main
git branch -M main

# Configure Remote
git remote remove origin 2>$null
git remote add origin https://github.com/sthanna/GlycoConjVacEpitopeMapper.git

# Push
git push -u origin main

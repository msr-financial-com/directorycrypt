#!/bin/bash

# Add post-checkout script that will decrypt everything when checking out
cat <<EOF > .git/hooks/post-checkout
#!/bin/bash

python main.py -d -k \$(pass show production/certs_encryption_key) -f "*"

EOF

# Add pre-commit script that will encrypt everything when commting
cat <<EOF > .git/hooks/pre-commit
#!/bin/bash

python main.py -e -k \$(pass show production/certs_encryption_key) -f "*"
git add -A
EOF

# Grant executions rights on these scripts
chmod +x .git/hooks/post-checkout
chmod +x .git/hooks/pre-commit

# Checkout the main branch, to decrypt everything
git checkout main

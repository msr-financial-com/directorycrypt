#!/bin/bash

cat <<EOF > .git/hooks/post-checkout
#!/bin/bash

python main.py -d -k \$(pass show production/certs_encryption_key) -f "*"

EOF

cat <<EOF > .git/hooks/pre-commit
#!/bin/bash

python main.py -e -k \$(pass show production/certs_encryption_key) -f "*"
git add -A
EOF

chmod +x .git/hooks/post-checkout
chmod +x .git/hooks/pre-commit

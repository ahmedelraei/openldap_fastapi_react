#!/bin/bash

# OpenLDAP entrypoint
# Creates essential structure and default users

set -e

echo "Starting OpenLDAP with custom initialization..."

# Function to wait for LDAP and apply LDIF files
apply_ldif_files() {
    echo "Waiting for LDAP server to be ready..."
    
    # Wait for LDAP to be ready
    for i in {1..30}; do
        if ldapwhoami -x -H ldap://localhost:1389 -D "cn=admin,dc=example,dc=com" -w admin123 >/dev/null 2>&1; then
            echo "LDAP server is ready"
            break
        fi
        echo "Waiting for LDAP... ($i/30)"
        sleep 2
    done
    
    # Apply LDIF files
    if [ -d "/ldif" ]; then
        echo "Applying LDIF files..."
        for ldif_file in /ldif/*.ldif; do
            if [ -f "$ldif_file" ]; then
                echo "Applying $(basename "$ldif_file")..."
                ldapadd -x -H ldap://localhost:1389 -D "cn=admin,dc=example,dc=com" -w admin123 -f "$ldif_file" || echo "LDIF already applied or failed: $(basename "$ldif_file")"
            fi
        done
    fi
    
    echo "LDAP initialization completed!"
}

# Run LDIF application in background after LDAP starts
apply_ldif_files &

# Start OpenLDAP
exec /opt/bitnami/scripts/openldap/entrypoint.sh /opt/bitnami/scripts/openldap/run.sh

FROM bitnami/openldap:2.6.10

# Switch to root user for setup
USER root

# Install ldap-utils for ldif processing
RUN apt-get update && \
    apt-get install -y ldap-utils && \
    rm -rf /var/lib/apt/lists/*

# Copy LDIF files for initialization
COPY ldif/ /ldif/

# Copy custom entrypoint
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set environment variables
ENV LDAP_ADMIN_USERNAME=admin
ENV LDAP_ADMIN_PASSWORD=admin123
ENV LDAP_ROOT=dc=example,dc=com
ENV LDAP_ADMIN_DN=cn=admin,dc=example,dc=com
ENV LDAP_SKIP_DEFAULT_TREE=yes
ENV LDAP_EXTRA_SCHEMAS=cosine,inetorgperson,nis

# Use custom entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

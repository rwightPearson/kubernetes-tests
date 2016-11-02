FROM bitesize-registry.default.svc.cluster.local:5000/baseimages/ubuntu-httpdfcgi:1.3
MAINTAINER Bitesize Project <bitesize-techops@pearson.com>
RUN echo 'deb http://apt/ bitesize main' > /etc/apt/sources.list.d/bitesize.list
RUN apt-get -q update && apt-get install -y --force-yes ruby2.0 ruby-dev gcc make git-all jq  certs=1.0-*  testrunner=1.0-* jmespath docutils python-dateutil futures s3transfer botocore boto3 nose2 pyyaml rubygem-json rubygem-mixlib-shellout rubygem-net-ssh rubygem-net-scp rubygem-ffi rubygem-gssapi rubygem-httpclient rubygem-rubyntlm rubygem-little-plugger rubygem-multi-json rubygem-logging rubygem-nori rubygem-builder rubygem-gyoku rubygem-erubis rubygem-winrm rubygem-rubyzip rubygem-winrm-fs rubygem-excon rubygem-docker-api rubygem-train rubygem-thor rubygem-rainbow rubygem-method-source rubygem-rspec-support rubygem-rspec-core rubygem-diff-lcs rubygem-rspec-expectations rubygem-rspec-mocks rubygem-rspec rubygem-rspec-its rubygem-coderay rubygem-slop rubygem-pry rubygem-hashie rubygem-mixlib-log rubygem-sslshake rubygem-inspec bats  && rm -rf /var/cache/apt


ENTRYPOINT ["/var/run.sh"]

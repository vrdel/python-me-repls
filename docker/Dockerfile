FROM centos:7
MAINTAINER dvrcic@srce.hr
RUN groupadd user -g 1000 && useradd -u 1000 -g 1000 user -m -d /home/user -s /bin/zsh
RUN yum -y update; yum clean all
RUN yum -y install epel-release && \
    yum -y install \
			htop \
      ack \
      ctags \
      fortune-mod \
      git \
      iproute \
      make \
      mc \
      net-tools \
      python-devel \
      python-pip \
      python-setuptools \
      python3-devel \
      python3-setuptools \
      rpmdevtools \
      sshd \
      sudo \
      the_silver_searcher \
      tmux \
      vim \
      wget \
      yum-utils \
      zsh
RUN pip install -U pip; pip3 install -U pip
RUN pip2 install wheel ipdb==0.10 setuptools; pip3 install -U wheel ipdb setuptools
RUN passwd -d root
RUN wget https://raw.githubusercontent.com/vrdel/my-vm-customize/master/centos7/argo-devel.repo -O /etc/yum.repos.d/argo-devel.repo
COPY rpms/* /home/user/aio-libs/
RUN yum -y localinstall /home/user/aio-libs/*
RUN echo "user ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers
USER user
WORKDIR /home/user
RUN curl -sfL https://git.io/chezmoi | sh
CMD ["/bin/zsh"]

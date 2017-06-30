# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = flask-glass
SOURCEDIR     = .
BUILDDIR      = _build

AUTOBUILDOPT  = -r '.ropeproject/.*' -r '.git/.*' -r '.idea/.*' -B

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

live:
	sphinx-autobuild -b html $(SPHINXOPTS) $(AUTOBUILDOPT) "$(SOURCEDIR)" "$(BUILDDIR)/html"


.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

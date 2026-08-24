PLAY := playbooks/10-install.yml
PLAY2 := playbooks/20-hardening.yml
MANIFEST := ../os/archlinux/manifest.yaml

.PHONY: lint syntax check run run-phase2

lint:
	yamllint -c .yamllint .
	ansible-lint playbooks/ roles/

syntax:
	ansible-playbook --syntax-check $(PLAY)
	ansible-playbook --syntax-check $(PLAY2)

check:
	python3 generators/manifest_to_playbook.py --check --manifest $(MANIFEST)

run:
	ansible-playbook $(PLAY) --confirm-destructive

run-phase2:
	ansible-playbook $(PLAY2)

PLAY := playbooks/10-install.yml
PLAY2 := playbooks/20-hardening.yml
PLAY3 := playbooks/30-desktop.yml
PLAY4 := playbooks/40-workflow.yml
MANIFEST := ../os/archlinux/manifest.yaml

.PHONY: lint syntax check run run-phase2 run-phase3 run-phase4

lint:
	yamllint -c .yamllint .
	ansible-lint playbooks/ roles/

syntax:
	ansible-playbook --syntax-check $(PLAY)
	ansible-playbook --syntax-check $(PLAY2)
	ansible-playbook --syntax-check $(PLAY3)
	ansible-playbook --syntax-check $(PLAY4)

check:
	python3 generators/manifest_to_playbook.py --check --manifest $(MANIFEST)

run:
	ansible-playbook $(PLAY) --confirm-destructive

run-phase2:
	ansible-playbook $(PLAY2)

run-phase3:
	ansible-playbook $(PLAY3)

run-phase4:
	ansible-playbook $(PLAY4)

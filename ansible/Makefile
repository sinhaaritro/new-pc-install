PLAY := playbooks/10-install.yml
MANIFEST := ../os/archlinux/manifest.yaml

.PHONY: lint syntax check run

lint:
	yamllint -c .yamllint .
	ansible-lint playbooks/ roles/

syntax:
	ansible-playbook --syntax-check $(PLAY)

check:
	python3 generators/manifest_to_playbook.py --check --manifest $(MANIFEST)

run:
	ansible-playbook $(PLAY) --confirm-destructive

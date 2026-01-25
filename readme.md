# Compose

Docker compose pour déploiement. Chaque service est déployé via [Komo.do](https://komo.do/) depuis un dépot local.

# Sommaire

- [Stack réseau](#stack-réseau)
  - [AdGuard](#adguard)
  - [Wazuh AGENT](#wazuh-agent)
- [Stack cloud](#stack-cloud)
  - [Authentik](#authentik)
  - [Immich](#immich)
  - [Vaultwarden](#vaultwarden)
  - [Linkwarden](#linkwarden)
- [Stack monitoring](#stack-monitoring)
  - [Ntfy](#ntfy)
  - [Plausible](#plausible)
  - [Grafana](#grafana)
- [Stack médias](#stack-médias)
  - [QBitTorrent](#qbittorrent)
  - [Jellyfin (Nvidia GPU)](#jellyfin-avec-transcodage-nvidia)
- [Stack LLM](#stack-llm)
  - [Ollama + OpenWebUI](#ollama--openwebui)


# Services déployés :

## Stack réseau :

### AdGuard

    AdGuard est un service de DNS complet avec GUI, blocages, réécritures DNS. Supporte DoH, DoT ou encore Quic.

- Fichiers: [`adguard/compose.yaml`](adguard/compose.yaml)
- Tutoriels: SOON
- Site du projet: [AdGuard.com](https://adguard.com/fr/adguard-home/overview.html)
- Code source: [GH AdGuard](https://github.com/AdguardTeam/AdGuardHome)

### Wazuh AGENT

    Wazuh est une plateforme de surveillance et de réponse aux évènements d'une infrastructure.

- Fichiers: [`wazuh/agent-compose.yaml`](wazuh/agent-compose.yaml)
- Tutoriels: SOON
- Site du projet: [Wazuh.com](https://wazuh.com/)
- Code source: [GH Wazuh](https://github.com/Wazuh/Wazuh)

### Nginx (Swag)

    Nginx est utilisé comme reverse-proxy et gestionnaire de certificats. Swag l'améliore avec la gestion des certificats et divers mods.

- Fichiers: [`nginx/compose.yaml`](nginx/compose.yaml)
- Tutoriels: [SWAG](https://docu.adenyrr.me/reseau/swag.html)
- Site du projet: [nginx](https://nginx.org/)
- Code source: [GH Nginx](https://github.com/nginx/nginx)

## Stack cloud :

### Authentik

    Authentik permet de centraliser la configuration des identifiants en un point unique. SSO, LDAP, OICD, ...

- Fichiers: [`authentik/compose.yaml`](authentik/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Authentik.io](https://goauthentik.io/)
- Code source: [GH Authentik](https://github.com/goauthentik/authentik)

### Immich

    Immich est un gestionnaire de sauvegardes photos et vidéos, avec applications mobiles.

- Fichiers: [`immich/compose.yml`](immich/compose.yml)
- Tutoriels: SOON
- Site du projet: [Immich.app](https://immich.app/)
- Code source: [GH Immich](https://github.com/immich-app/immich)

### Vaultwarden

    Vaultwarden est un fork de Bitwarden, le gestionnaire de mot de passe.

- Fichiers: [`vaultwarden/compose.yaml`](vaultwarden/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Vaultwarden.net](https://www.vaultwarden.net/)
- Code source: [GH Vaultwarden](https://github.com/dani-garcia/vaultwarden)

### Linkwarden

    Linkwarden est un manager de marque-pages. Il permet de sauvegarder, trier et consulter plus tard des liens.

- Fichiers: [`linkwarden/compose.yml`](linkwarden/compose.yml)
- Tutoriels: SOON
- Site du projet: [Linkwarden.app](https://linkwarden.app/)
- Code source: [GH Linkwarden](https://github.com/linkwarden/linkwarden)

## Stack monitoring

### Ntfy

    Ntfy permet de recevoir des alertes en cas d'évènements prédéfinis.

- Fichiers: [`ntfy/compose.yaml`](ntfy/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Ntfy.sh](https://ntfy.sh/)
- Code source: [GH ntfy](https://github.com/binwiederhier/ntfy)

### Plausible

    Plausible permet de consulter les statistiques de visite de ses sites en étant RGPD-friendly.

- Fichiers: [`plausible/compose.yaml`](plausible/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Plausible.io](https://plausible.io/)
- Code source: [GH Plausible](https://github.com/plausible/community-edition)

### Grafana

    Grafana permet de mettre en forme de manière complètement libre les données récoltées par d'autres sources.

- Fichiers: [`grafana/compose.yaml`](grafana/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Grafana.com](https://grafana.com/)
- Code source: [GH Grafana](https://github.com/grafana/grafana)

## Stack médias :

### QBitTorrent

    Qbittorrent est un logiciel de gestion de téléchargements par torrents, basé sur Qt et supportant des milliers de fichiers.

- Fichiers: [`qbittorrent/compose.yaml`](qbittorrent/compose.yaml)
- Tutoriels: SOON
- Site du projet: [qbittorrent.org](https://www.qbittorrent.org/)
- Code source: [GH Qbittorrent](https://github.com/qbittorrent/qBittorrent/)

### Jellyfin (avec transcodage nvidia)

    Jellyfin est une plateforme de streaming entièrement autohébergée, similaire à Plex.

- Fichiers: [`jellyfin/compose.yaml`](jellyfin/compose.yaml)
- Tutoriels: [become.sh](https://docs.become.sh/services/jellyfin/)
- Site du projet: [Jellyfin.org](https://jellyfin.org/)
- Code source: [GH Jellyfin](https://github.com/jellyfin/jellyfin)

## Stack LLM :

### Ollama + OpenWebUI

    Ollama est une plateforme permettant de télécharger et utiliser des LLM. OpenWebUI est une interface de gestion d'Ollama permettant d'utiliser outils, fonctions, RAG, chatbot et plus encore.

- Fichiers: [`ollama/compose.yaml`](ollama/compose.yaml)
- Tutoriels: [become.sh](https://docs.become.sh/services/ollama/)
- Site du projet: [Ollama.com](https://ollama.com/) && [OpenWebUI.com](https://openwebui.com/)
- Code source: [GH Ollama](https://github.com/ollama/ollama) && [GH OpenWebUI](https://github.com/open-webui/open-webui)

## Autres services

### Excalidraw

    Excalidraw fournit un tableau blanc collaboratif simple et rapide.

- Fichiers: [`excalidraw/compose.yaml`](excalidraw/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Excalidraw](https://excalidraw.com/)
- Code source: [GH Excalidraw](https://github.com/excalidraw/excalidraw)

### LibreChat

    LibreChat propose une interface self-hosted pour LLMs et chatbots.

- Fichiers: [`librechat/compose.yaml`](librechat/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### SearxNG

    SearxNG est un méta-moteur de recherche respectueux de la vie privée.

- Fichiers: [`searxng/compose.yaml`](searxng/compose.yaml)
- Tutoriels: SOON
- Site du projet: [SearxNG](https://searx.github.io/searxng/)
- Code source: [GH SearxNG](https://github.com/searxng/searxng)

### Open Notebook

    Environnement pour notebooks et outils pédagogiques.

- Fichiers: [`open-notebook/compose.yaml`](open-notebook/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### Donetick

    Donetick est un outil de gestion de tâches léger.

- Fichiers: [`donetick/compose.yaml`](donetick/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### Zipline

    Zipline regroupe des utilitaires divers pour l'infrastructure.

- Fichiers: [`zipline/compose.yaml`](zipline/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### Statping-NG

    Statping-NG permet de surveiller la disponibilité et latence des services.

- Fichiers: [`statping-ng/compose.yaml`](statping-ng/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### Affine

    Affine est une application (ex: gestion de notes/collaboration) incluse pour déploiement.

- Fichiers: [`affine/compose.yaml`](affine/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### Actual

    Répertoire d'exemples ou services auxiliaires ("actual").

- Fichiers: [`actual/compose.yaml`](actual/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON
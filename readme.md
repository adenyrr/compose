# Sommaire

- [Sommaire](#sommaire)
- [Services déployés :](#services-déployés-)
  - [Stack déploiement](#stack-déploiement)
    - [Gitlab](#gitlab)
    - [Komodo](#komodo)
    - [Semaphore](#semaphore)
    - [Termix](#termix)
  - [Stack réseau :](#stack-réseau-)
    - [AdGuard](#adguard)
    - [Nginx (Swag)](#nginx-swag)
    - [ACME (smallstep)](#acme-smallstep)
    - [Scanopy](#scanopy)
    - [Speedtest](#speedtest)
  - [Stack cloud :](#stack-cloud-)
    - [Authentik](#authentik)
    - [Immich](#immich)
    - [Vaultwarden](#vaultwarden)
    - [Actual](#actual)
    - [Opencloud](#opencloud)
  - [Stack monitoring](#stack-monitoring)
    - [Ntfy](#ntfy)
    - [Plausible](#plausible)
    - [Grafana](#grafana)
    - [Prometheus](#prometheus)
    - [Promere](#promere)
  - [Stack médias :](#stack-médias-)
    - [QBitTorrent](#qbittorrent)
    - [Jellyfin (avec transcodage nvidia)](#jellyfin-avec-transcodage-nvidia)
    - [Qui](#qui)
    - [Tracearr](#tracearr)
    - [jellystats](#jellystats)
    - [Jellyserr](#jellyserr)
  - [Stack LLM :](#stack-llm-)
    - [Ollama + OpenWebUI](#ollama--openwebui)
    - [SearxNG](#searxng)
    - [N8n](#n8n)
  - [Stack frontend](#stack-frontend)
    - [Linkwarden](#linkwarden)
    - [Statping-NG](#statping-ng)
    - [Wisherr](#wisherr)
    - [Donetick](#donetick)
    - [Gethompage](#gethompage)
  - [Autres services](#autres-services)
    - [Excalidraw](#excalidraw)


# Services déployés :

Docker compose pour déploiement. Chaque service est déployé via [Komo.do](https://komo.do/) depuis un dépot local.

## Stack déploiement

### Gitlab

    AdGuard est un service de DNS complet avec GUI, blocages, réécritures DNS. Supporte DoH, DoT ou encore Quic.

- Fichiers: [`adguard/compose.yaml`](adguard/compose.yaml)
- Tutoriels: SOON
- Site du projet: [AdGuard.com](https://adguard.com/fr/adguard-home/overview.html)
- Code source: [GH AdGuard](https://github.com/AdguardTeam/AdGuardHome)

### Komodo

    AdGuard est un service de DNS complet avec GUI, blocages, réécritures DNS. Supporte DoH, DoT ou encore Quic.

- Fichiers: [`adguard/compose.yaml`](adguard/compose.yaml)
- Tutoriels: SOON
- Site du projet: [AdGuard.com](https://adguard.com/fr/adguard-home/overview.html)
- Code source: [GH AdGuard](https://github.com/AdguardTeam/AdGuardHome)

### Semaphore

### Termix 

## Stack réseau :

### AdGuard

    AdGuard est un service de DNS complet avec GUI, blocages, réécritures DNS. Supporte DoH, DoT ou encore Quic.

- Fichiers: [`adguard/compose.yaml`](adguard/compose.yaml)
- Tutoriels: SOON
- Site du projet: [AdGuard.com](https://adguard.com/fr/adguard-home/overview.html)
- Code source: [GH AdGuard](https://github.com/AdguardTeam/AdGuardHome)


### Nginx (Swag)

    Nginx est utilisé comme reverse-proxy et gestionnaire de certificats. Swag l'améliore avec la gestion des certificats et divers mods.

- Fichiers: [`nginx/compose.yaml`](nginx/compose.yaml)
- Tutoriels: [SWAG](https://docu.adenyrr.me/reseau/swag.html)
- Site du projet: [nginx](https://nginx.org/)
- Code source: [GH Nginx](https://github.com/nginx/nginx)

### ACME (smallstep)

### Scanopy

### Speedtest

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

### Actual

    Application de budgetisation et tracking de dépenses.

- Fichiers: [`actual/compose.yaml`](actual/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON


### Opencloud

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

### Prometheus

### Promere

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


### Qui

### Tracearr

### jellystats

### Jellyserr

## Stack LLM :

### Ollama + OpenWebUI

    Ollama est une plateforme permettant de télécharger et utiliser des LLM. OpenWebUI est une interface de gestion d'Ollama permettant d'utiliser outils, fonctions, RAG, chatbot et plus encore.

- Fichiers: [`ollama/compose.yaml`](ollama/compose.yaml)
- Tutoriels: [become.sh](https://docs.become.sh/services/ollama/)
- Site du projet: [Ollama.com](https://ollama.com/) && [OpenWebUI.com](https://openwebui.com/)
- Code source: [GH Ollama](https://github.com/ollama/ollama) && [GH OpenWebUI](https://github.com/open-webui/open-webui)

### SearxNG

    SearxNG est un méta-moteur de recherche respectueux de la vie privée.

- Fichiers: [`searxng/compose.yaml`](searxng/compose.yaml)
- Tutoriels: SOON
- Site du projet: [SearxNG](https://searx.github.io/searxng/)
- Code source: [GH SearxNG](https://github.com/searxng/searxng)

### N8n

## Stack frontend

### Linkwarden

    Linkwarden est un manager de marque-pages. Il permet de sauvegarder, trier et consulter plus tard des liens.

- Fichiers: [`linkwarden/compose.yml`](linkwarden/compose.yml)
- Tutoriels: SOON
- Site du projet: [Linkwarden.app](https://linkwarden.app/)
- Code source: [GH Linkwarden](https://github.com/linkwarden/linkwarden)

### Statping-NG

    Statping-NG permet de surveiller la disponibilité et latence des services.

- Fichiers: [`statping-ng/compose.yaml`](statping-ng/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### Wisherr

### Donetick

    Donetick est un outil de gestion de tâches léger.

- Fichiers: [`donetick/compose.yaml`](donetick/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### Gethompage

## Autres services

### Excalidraw

    Excalidraw fournit un tableau blanc collaboratif simple et rapide.

- Fichiers: [`excalidraw/compose.yaml`](excalidraw/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Excalidraw](https://excalidraw.com/)
- Code source: [GH Excalidraw](https://github.com/excalidraw/excalidraw)
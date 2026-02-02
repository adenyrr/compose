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
    - [Alexandrie](#alexandrie)
    - [Opencloud](#opencloud)
    - [Kurrier](#kurrier)
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

    Gitlab est un service de forge GIT alternative à github.

- Fichiers: [`gitlab/compose.yaml`](gitlab/compose.yaml)
- Tutoriels: SOON
- Site du projet: [AGitlab.com](https://gitlab.com/adenyrr)
- Code source: [Gitlab](https://gitlab.com/gitlab-org/gitlab)

### Komodo

    Komodo est un service de déploiement de conteneurs à la GitOps.

- Fichiers: [`komodo/compose.yaml`](komodo/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Komo.do](https://komo.do)
- Code source: [GH Komodo](https://github.com/moghtech/komodo)

### Semaphore

    SemaphoreUI permet de lancer des scripts ansible, terraform ou opentofu.

- Fichiers: [`semaphore/compose.yaml`](semaphore/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Komo.do](https://komo.do)
- Code source: [GH AdGuard](https://github.com/moghtech/komodo)

### Termix 

    Termix est un utilitaire de multiples connexions SSH

- Fichiers: [`termix/compose.yaml`](termix/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Termix.site](https://termix.site)
- Code source: [GH Termix](https://github.com/Termix-SSH/Termix)

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

    ACME fourni des certificats internes et un endpoint ACME pour la fourniture automatisée de certificats

- Fichiers: [`acme/compose.yaml`](acme/compose.yaml)
- Tutoriels: SOON
- Site du projet: [smallstep.com](https://smallstep.com/)
- Code source: [GH Smallstep](https://github.com/smallstep)

### Scanopy

    Scanopy permet de diagrammer son réseau local

- Fichiers: [`scanopy/compose.yaml`](scanopy/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Scanopy.net](https://scanopy.net)
- Code source: [GH Scanopy](https://github.com/scanopy/scanopy)

### Speedtest

    Speedtest exterieur periodique avec suivi complet des statistiques

- Fichiers: [`speedtest/compose.yaml`](speedtest/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Speedtest-Tracker.dev](https://docs.speedtest-tracker.dev/)
- Code source: [GH SpeedTest](github.com/alexjustesen/speedtest-tracker)

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

### Alexandrie

    Application de prise de notes sous format markdown avec PWA.

- Fichiers: [`alexandrie/compose.yaml`](alexandrie/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Alexandrie-hub.fr](https://alexandrie-hub.fr/)
- Code source: [GH Alexandrie](https://github.com/Smaug6739/Alexandrie)

### Opencloud

    Gestion de fichiers, synchronisation, répertoires distants ...

- Fichiers: [`opencloud/compose.yaml`](opencloud/compose.yaml)
- Tutoriels: SOON
- Site du projet: [OpenCloud.eu](https://opencloud.eu)
- Code source: [GH OpenCloud](https://github.com/opencloud-eu/opencloud)

### Kurrier

    Kurrier est un service de gestion et d'envoi de messages (emails/notifications) destiné aux applications self-hosted, fournissant relais, templates et suivi des envois.

- Fichiers: [`kurrier/compose.yaml`](kurrier/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Kurrier.org](https://www.kurrier.org/)
- Code source: [GH Kurrier](https://github.com/kurrier-org/kurrier)

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

    Prometheus est un système de surveillance et de collecte de métriques largement utilisé pour le monitoring d'infrastructures et d'applications.

- Fichiers: [`prometheus/compose.yaml`](prometheus/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Prometheus.io](https://prometheus.io/)
- Code source: [GH Prometheus](https://github.com/prometheus/prometheus)

### Promere

    Interface visuelle légère de gestion d'environnements basés sur prometheus.

- Fichiers: [`promere/compose.yaml`](promere/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: [GH Promere](https://github.com/Leumas-LSN/promere-prometheus-manager)

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

    Qui est une surcouche à qbittorrent

- Fichiers: [`qui/compose.yaml`](qui/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: 

### Tracearr

    Tracearr traque les connexions utilisateurs sur plex, jellyfin, ...

- Fichiers: [`tracearr/compose.yaml`](tracearr/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### jellystats

    Jellystats collecte et présente des statistiques d'utilisation pour Jellyfin et services médias associés.

- Fichiers: [`jellystats/compose.yaml`](jellystats/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### Jellyserr

    Jellyserr fournit des outils complémentaires pour Jellyfin (notifications, rapports d'erreurs, intégrations externes).

- Fichiers: [`jellyserr/compose.yaml`](jellyserr/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

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

    n8n est un outil d'automatisation et d'orchestration de workflows visuels (intégration d'APIs, transformations, automatisations cron).

- Fichiers: [`n8n/compose.yaml`](n8n/compose.yaml)
- Tutoriels: SOON
- Site du projet: [n8n.io](https://n8n.io/)
- Code source: [GH n8n](https://github.com/n8n-io/n8n)

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

    Wisherr est une application frontend légère pour gérer des listes de souhaits, favoris ou listes d'achets.

- Fichiers: [`wisherr/compose.yaml`](wisherr/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### Donetick

    Donetick est un outil de gestion de tâches léger.

- Fichiers: [`donetick/compose.yaml`](donetick/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

### Gethompage

    Gethompage est une petite application de génération/gestion de pages d'accueil personnelles ou de landing pages simples.

- Fichiers: [`gethomepage/compose.yaml`](gethomepage/compose.yaml)
- Tutoriels: SOON
- Site du projet: SOON
- Code source: SOON

## Autres services

### Excalidraw

    Excalidraw fournit un tableau blanc collaboratif simple et rapide.

- Fichiers: [`excalidraw/compose.yaml`](excalidraw/compose.yaml)
- Tutoriels: SOON
- Site du projet: [Excalidraw](https://excalidraw.com/)
- Code source: [GH Excalidraw](https://github.com/excalidraw/excalidraw)
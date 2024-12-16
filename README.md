# TextBoard Bot

Ce bot a été conçu dans le cadre de l'expérience d'Aywen sur [TextBoard.fr](https://textboard.fr).

Grâce à sa connexion directe au protocole WebSocket, ce script offre des performances optimales et une réactivité inégalée pour interagir avec la plateforme.

## Fonctionnalités

- ✅ Gestion des threads
- ✅ Prise en charge de tous les types de caractères
- ✅ Fonctionnement continu avec reprise automatique après un crash

## Problèmes courants

### 1. J'ai un écran blanc, que faire ?

Si vous voyez un écran blanc, cela signifie probablement que vous utilisez le même compte Google pour le bot et pour visualiser votre dessin. Cependant, une seule connexion WebSocket (WS) est autorisée par compte. Pour résoudre ce problème, utilisez un compte Google alternatif pour le bot.

### 2. Je ne vois pas mon dessin

Si vous ne voyez pas votre dessin ou si plusieurs erreurs apparaissent :

- Vérifiez que vous avez correctement entré votre **token JWT**.
- Assurez-vous que les coordonnées sont correctement configurées.

![exemple](./image.png)

## Installation

Clonez le dépot

```bash
git clone <url>
```

Installez dépendances.

```bash
pip install -r requirements.txt
```

## Utilisation

1. **Configuration** :

   Créez un fichier `.env` à l'extérieur du dossier `src` et ajoutez-y les variables suivantes :

   ```env
   X_INIT=-694               # Variable X
   Y_INIT=-699               # Variable Y

   TOKEN_JWT="SECRET"        # Token JWT - ne jamais partager
   WS_TIMEOUT=4              # Temps de timeout WebSocket
   MESSAGE_DELAY_SECOND=0.03 # Délai des messages en secondes

   ASCII_ART=""              # Votre art ASCI
   ```

2. **Exécution** :
   Lancez le bot avec la commande suivante :

```bash
python main.py
```

## Contribution

Les contributions sont les bienvenues! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

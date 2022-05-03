#!/usr/bin/env bash

# qr-gpg.sh
# Usage: ./qr-gpg.sh clear-sign "MESSAGE
#        ./qr-gpg.sh clear-sign "MESSAGE" FILE.png
#        ./qr-gpg.sh verify-clear-sign FILE.png
#        ./qr-gpg.sh verify-clear-sign FILE.png OUTPUT.txt

DATE=`date '+%s-%N'`
NANO=`date '%N'`
if [ -z "$3" ]
  then
    FILENAME=msg_$.png
  else
    FILENAME=$3
fi

if [ $# -lt 2 ] ; then
    printf 'Usage: ./qr-gpg.sh clear-sign "MESSAGE"\n'
    printf '       ./qr-gpg.sh clear-sign "MESSAGE" FILE.png\n'
    printf '       ./qr-gpg.sh verify-clear-sign FILE.png\n'
    printf '       ./qr-gpg.sh verify-clear-sign FILE.png OUTFILE\n'
    exit 1
fi

if [ $1 = "clear-sign" ] && [ $# -gt 1 ] ; then
    printf "$2">msg_$DATE
    gpg --clear-sign --armor msg_$DATE
    rm msg_$DATE
    cat msg_$DATE.asc|qrencode -o $FILENAME
    rm msg_$DATE.asc
    printf "Message gpg clear-signed and encoded as a qr-code and output to file: $FILENAME \n"
fi

if [ $1 = "verify-clear-sign" ] && [ $# -eq 2 ] ; then
    FILENAME=$2
    printf "Decoding QR-Code: \n"
    zbarimg $FILENAME -q>msg_$DATE.asc
    sed -i.bak s/QR-Code://g msg_$DATE.asc
    cat msg_$DATE.asc
    printf "Verifying Signature: \n"
    gpg --verify msg_$DATE.asc
    MESSAGE="$(sed -n '/Hash:.*/,/-----BEGIN PGP SIGNATURE-----/{/Hash:.*/n;/-----BEGIN PGP SIGNATURE-----/n;p}' msg_$DATE.asc)"
    printf "\n"
    printf "Message: ${MESSAGE}\n"
    rm msg_$DATE.asc msg_$DATE.asc.bak
fi

if [ $1 = "verify-clear-sign" ] && [ $# -eq 3 ] ; then
    FILENAME=$2
    OUTFILE=$3
    printf "Decoding QR-Code: \n">>$OUTFILE
    zbarimg $FILENAME -q>>msg_$DATE.asc
    sed -i.bak s/QR-Code://g msg_$DATE.asc
    cat msg_$DATE.asc>>$OUTFILE
    printf "Verifying Signature: \n">>$OUTFILE
    gpg --verify --armor --logger-fd 1 msg_$DATE.asc>>$OUTFILE
    MESSAGE="$(sed -n '/Hash:.*/,/-----BEGIN PGP SIGNATURE-----/{/Hash:.*/n;/-----BEGIN PGP SIGNATURE-----/n;p}' msg_$DATE.asc)"
    printf "\n">>$OUTFILE
    printf "Message: ${MESSAGE}\n">>$OUTFILE
    rm msg_$DATE.asc msg_$DATE.asc.bak
    printf "qr-code contents, gpg verification status, and message were output to file: $FILENAME \n"
fi

ConfDir=$1
ConfFile=$2
SubFile=$3

while read line
do
	InFile=$line
	echo "working on ${InFile}"
	python ConfSubInReplace.py $ConfDir/$ConfFile $InFile conf $ConfDir/${ConfFile}_${InFile}
	python ConfSubInReplace.py $SubFile ${ConfFile}_${InFile} sub ${SubFile}_$InFile
	python TheOneForAll.py $ConfDir/${ConfFile}_${InFile} ${SubFile}_$InFile
	condor_submit ${SubFile}_${InFile}MULPARA
done

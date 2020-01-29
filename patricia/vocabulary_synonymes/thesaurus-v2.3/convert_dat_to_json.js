const data = fs.readFileSync('./thes_fr.dat', 'utf8');

const lines = data.split("\n");

let o = {};
for(let i = 0; lines.length > i ; i = i + 2){
    if(lines[i+1]){
        o[lines[i].split("|")[0]]= lines[i+1].split("|").slice(1);
    }
}

fs.writeFileSync('./dic_synonimes.json', JSON.stringify(o, null, 2));



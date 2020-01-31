
// const fs = require('fs');

// Commande : node chercher_synonimes {mot à chercher} 
//
// exemple : 
// node cherche_synonimes danser
// resultat :
// [
//     'chalouper',
//     'frétiller',
//     'sautiller',
//     'gambader',
//     'trémousser',
//     'sauter',
//     'valser'
// ]


const fs = require('fs');
const dic = JSON.parse(fs.readFileSync('./dic_synonymes.json', 'utf8'));

console.log(dic[process.argv[2]]);



var fs = require('fs');

// var file = fs.readFileSync("./dic_phonetique_fr_FR.txt", 'utf8');

// console.log(file.length);

// var lines = file.split("\n");

// console.log(lines.length);

// var dic = {};

// lines.map((value)=>{
//     var d = value.split("\t");
//     dic[d[0]]= d[1];
// });

// fs.writeFileSync("./dic_phonetique_fr_FR.json", JSON.stringify(dic, null, 2));

var file = fs.readFileSync("./dic_phonetique_fr_FR.json", 'utf8');
var dic = JSON.parse(file);


console.log(dic["envoyé"]);
console.log(dic["envoyais"]);
console.log(dic["envoyaient"]);
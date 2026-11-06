const fs = require("fs");
const path = require("path");
const src = __dirname;
const dest = path.join(__dirname, "www");
fs.mkdirSync(dest, {recursive:true});
for (const file of ["index.html","style.css","app.js"]) {
  fs.copyFileSync(path.join(src,file), path.join(dest,file));
}
console.log("Web assets copied to www/");

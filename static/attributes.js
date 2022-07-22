var limit = 7;
var count = 4;



function addCatAttribute() {

  var catVars = document.getElementById('cat_vars')
  var values = ["None","Primary Type", "Secondary Type", "Generation", "Species", "Number of Abilities", "Growth Rate", "Egg Type"];

  var select = document.createElement("select");
  select.name = "catVar";
  select.id = "catVar";

  for (const val of values)
  {
    
      var option = document.createElement("option");
      option.value = val;
      option.text = val.charAt(0) + val.slice(1);
      select.appendChild(option);
  }
  var label = document.createElement("label");
  label.innerHTML = "Search by Categorical Variable: "
  label.htmlFor = "catVar";

  document.getElementById("cat_vars").appendChild(label).appendChild(select);

}

function addBaseAttribute() {

  var catVars = document.getElementById('categorical_variables')
  var values = ["None","Primary Type", "Secondary Type", "Generation", "Species", "Number of Abilities", "Growth Rate", "Egg Type"];

  var select = document.createElement("select");
  select.name = "catVar";
  select.id = "catVar";

  for (const val of values)
  {
    
      var option = document.createElement("option");
      option.value = val;
      option.text = val.charAt(0) + val.slice(1);
      select.appendChild(option);
  }
  var label = document.createElement("label");
  label.innerHTML = "Search by Base Stats Variable: "
  label.htmlFor = "catVar";

  document.getElementById("cat_vars").appendChild(label).appendChild(select);

}
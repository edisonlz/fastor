{% if user_passes_test %}
window.onload = function() {
//    var divUserTools = document.getElementById("user-tools");
//    var aQBE = document.createElement("a");
//    var txtQBE = document.createTextNode('{{ qbe_label }}');
//    aQBE.setAttribute("href", "{{ qbe_url }}");
//    aQBE.appendChild(txtQBE);
//    var txtSeparator = document.createTextNode('/ ');
//    divUserTools.appendChild(txtSeparator);
//    divUserTools.appendChild(aQBE);

    var divContentRelated = document.getElementById("content-related");
    var divQBE = document.createElement("div")
    var aQBE = document.createElement("a");
    var txtQBE = document.createTextNode("{{ qbe_label }}");
    var h2QBE = document.createElement("h2");
    var h2QBEtxt = document.createTextNode("{{ reports_label }}");
    var h3QBE = document.createElement("h3");
    h2QBE.appendChild(h2QBEtxt);
    divQBE.appendChild(h2QBE);
    aQBE.setAttribute("href", "{{ qbe_url }}");
    aQBE.appendChild(txtQBE);
    h3QBE.appendChild(aQBE);
    divQBE.appendChild(h3QBE);
    divQBE.setAttribute("class", "module");
    divContentRelated.appendChild(divQBE);
}
{% endif %}

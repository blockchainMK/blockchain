var subProvince = {{dataCity|map(attribute=1)|list|tojson|safe}};
var subCity = {{dataCity|map(attribute=2)|list|tojson|safe}};

function checkProvince(province)
{
	var city = [];
	for (i=0; i<subProvince.length; i++)
	{
		if(subProvince[i]==province)
		{
		    city.push(subCity[i]);
		}
	}

	return city;
	// return {{dataCity|map(attribute=1)|list|tojson|safe}} == province;
}

function setOption()
{
	var valSelector = document.getElementById("provinsi").value;

	if(valSelector)
	{
		var selectionCity = checkProvince(valSelector);
	}

	document.getElementById("kabupatenkota").innerHTML = '<option value="" selected="selected" disabled>-- Pilih Kabupaten/Kota --</option>';
	// document.getElementById("test").innerHTML = selectionCity;
	if(selectionCity.length)
	{
		var html = '<option value="" selected="selected" disabled>-- Pilih Kabupaten/Kota --</option>';

		selectionCity.forEach(function(city)
		{
		    html += '<option value="'+city+'">'+city+'</option>';
		});
	}
	else
	{
		var html='<option value="" selected="selected" disabled>-- Pilih Kabupaten/Kota --</option>';
	}
	document.getElementById("kabupatenkota").innerHTML = html;
}

function setOption_()
{
	document.getElementById("provinsi").addEventListener("onchange", setOption());
}

var subCollege = {{dataCollege|map(attribute=1)|list|tojson|safe}};

function suggestion()
{
	document.getElementById("datalist").innerHTML = ''; 
	var l = document.getElementById("univOption").value.length;
				
	for (i=0; i<subCollege.length; i++)
	{
		if(((subCollege[i].toLowerCase()).indexOf(value.toLowerCase()))>-1) 
        {
            var node = document.createElement("option"); 
            var val = document.createTextNode(subColleges[i]); 
            node.appendChild(val); 
  
            document.getElementById("datalist").appendChild(node); 
        } 
    }
}

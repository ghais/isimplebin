function initPastebin()
{
	if (document.getElementById)
	{		
		var radio;
		
		radio=document.getElementById('expiry_day');
		if (radio)
		{
			radio.onclick=function ()
			{
				var expiryinfo=document.getElementById('expiryinfo');
				expiryinfo.innerHTML="Good for IRC or IM conversations";
				
				document.getElementById('expiry_day_label').className='current';
				document.getElementById('expiry_month_label').className='';
				document.getElementById('expiry_forever_label').className='';
			}
			if (radio.checked)
				radio.onclick();
		}
		
		radio=document.getElementById('expiry_month');
		if (radio)
		{
			radio.onclick=function ()
			{
				var expiryinfo=document.getElementById('expiryinfo');
				expiryinfo.innerHTML="Good for email conversations / temporary data";
			
				document.getElementById('expiry_day_label').className='';
				document.getElementById('expiry_month_label').className='current';
				document.getElementById('expiry_forever_label').className='';
			}
			if (radio.checked)
				radio.onclick();
		}
		
		radio=document.getElementById('expiry_forever');
		if (radio)
		{
			radio.onclick=function ()
			{
				var expiryinfo=document.getElementById('expiryinfo');
				expiryinfo.innerHTML="Good for long term archival of useful snippets";
			
				document.getElementById('expiry_day_label').className='';
				document.getElementById('expiry_month_label').className='';
				document.getElementById('expiry_forever_label').className='current';
			}
			if (radio.checked)
				radio.onclick();
		}
		
	}
	
}
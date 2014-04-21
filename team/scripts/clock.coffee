$(document).ready ->
	dateString = $('#timestamp').text()
	end = Date.parse(dateString)
	window.setInterval( 
		() ->
			delta = end - Date.now()
			
			format = (num) ->
				if num / 10 < 1
					return "0#{num}"
				return num

			seconds = Math.floor( (delta / 1000) % 60 )
			minutes = Math.floor( ((delta / (1000*60)) % 60) )
			hours   = Math.floor( ((delta / (1000*60*60))) )
			clockText = "#{format(hours)}:#{format(minutes)}:#{format(seconds)}"
			$('#time').text(clockText)



		, 500)
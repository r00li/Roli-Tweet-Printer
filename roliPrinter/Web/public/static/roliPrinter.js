$(document).ready(function() {

	$('#twitterUserAdd').on( "click", function() {
	    $('#twitterUserAdd').prop('disabled', true);
        addTwitterFollower($('#twitterInputDisplayName').val())
	});

	$('#twitterTestPrint').on( "click", function() {
	    $('#twitterTestPrint').prop('disabled', true);
        printTweetWithId($('#twitterInputTestTweetId').val())
	});

	$('#notePrint').on( "click", function() {
	    $('#notePrint').prop('disabled', true);
        printNote($('#note').val(), $('#noteQrData').val())
	});

	$('#redditSettingsSave').on( "click", function() {
	    $('#redditSettingsSave').prop('disabled', true);
        saveRedditSettings($('#redditClientId').val(), $('#redditClientSecret').val(), $('#redditRefreshToken').val())
	});

	$('#redditAuthorizeAccount').on( "click", function() {
	    $('#redditAuthorizeAccount').prop('disabled', true);
        getRedditAuthorizationURL();
	});

	$('#redditRequestToken').on( "click", function() {
	    $('#redditRequestToken').prop('disabled', true);
        getRedditRefreshToken($('#redditAuthorizationCode').val());
	});

	$('#globalSettingsSave').on( "click", function() {
	    $('#globalSettingsSave').prop('disabled', true);
        saveGlobalSettings(parseInt($('#usbPID').val(), 16), parseInt($('#usbVID').val(), 16));
	});

	$('#twitterSettingsSave').on( "click", function() {
	    $('#twitterSettingsSave').prop('disabled', true);
        saveTwitterSettings($('#twitterInputConsumerKey').val(), $('#twitterInputConsumerSecret').val(), $('#twitterInputAccessTokenKey').val(), $('#twitterInputAccessTokenSecret').val());
	});

	function editTwitterFollower(id, remove) {
		$.ajax({
			type: "POST",
			url: "/api/twitterModifyUser/" + id,
			data: JSON.stringify({"delete" : remove}),
			contentType: "application/json",
			dataType: "json",
			success: function (data) {
				console.log("Follower removed!");
				refreshDisplay();
			}
		}).fail(function(jqXHR, textStatus, errorThrown) {
			$('#infoModalContent').empty()
			$('#infoModalContent').append('Error deleting twitter user. Try again later!');
			$('#infoModal').modal('show');
		});
	}

	function addTwitterFollower(displayName) {
  		$.ajax({
			type: "POST",
			url: "/api/twitterFollow",
			data: JSON.stringify({"screenName" : displayName}),
			contentType: "application/json",
			dataType: "json",
			success: function (data) {
				console.log("Follower posted!");
				console.log(data);
				$('#twitterInputDisplayName').val('');
				$('#twitterUserAdd').prop('disabled', false);
				refreshDisplay();
			}
		}).fail(function(jqXHR, textStatus, errorThrown) {
			$('#twitterUserAdd').prop('disabled', false);

			$('#infoModalContent').empty()
			$('#infoModalContent').append('Error adding new twitter user. Check that the field is not empty and try again!');
			$('#infoModal').modal('show');
		});
  	}

  	function printTweetWithId(tweetId) {
  		$.ajax({
			type: "POST",
			url: "/api/twitterPrintTweetWithId/" + tweetId,
			contentType: "application/json",
			dataType: "json",
			success: function (data) {
				console.log("Follower posted!");
				console.log(data);
				$('#twitterInputTestTweetId').val('');
				$('#twitterTestPrint').prop('disabled', false);
				refreshDisplay();
			}
		}).fail(function(jqXHR, textStatus, errorThrown) {
			$('#twitterTestPrint').prop('disabled', false);

			$('#infoModalContent').empty()
			$('#infoModalContent').append('Error printing test tweet. Try again later!');
			$('#infoModal').modal('show');
		});
  	}

  	function saveTwitterSettings(consumerKey, consumerSecret, accessToken, accessTokenSecret) {
  		$.ajax({
			type: "POST",
			url: "/api/twitterSaveSettings",
			data: JSON.stringify({"consumerKey" : consumerKey, "consumerSecret" : consumerSecret, "accessToken" : accessToken, "accessTokenSecret" : accessTokenSecret}),
			contentType: "application/json",
			dataType: "json",
			success: function (data) {
				console.log("Twitter settings saved");

    			$('#twitterSettingsSave').prop('disabled', false);
				refreshDisplay();
			}
		}).fail(function(jqXHR, textStatus, errorThrown) {
			$('#twitterSettingsSave').prop('disabled', false);

			$('#infoModalContent').empty()
			$('#infoModalContent').append('Error saving twitter settings. Try again.');
			$('#infoModal').modal('show');
		});
  	}


  	function refreshDisplay() {
  	    $.ajax({
            type: "GET",
            url: "/api/settings",
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                console.log(data)
                settings = JSON.parse(data.settings)

                // Global settings
                $("#usbVID").val(settings.global.printerUSBVid.toString(16))
                $("#usbPID").val(settings.global.printerUSBPid.toString(16))

                // Twitter settings
                $("#twitterInputConsumerKey").val(settings.twitter.twitterConsumerKey)
                $("#twitterInputConsumerSecret").val(settings.twitter.twitterConsumerSecret)
                $("#twitterInputAccessTokenKey").val(settings.twitter.twitterAccessTokenKey)
                $("#twitterInputAccessTokenSecret").val(settings.twitter.twitterAccessTokenSecret)

                $('#followed').empty();
                $.each(settings.twitter.twitterFollowing, function (index) {
                    var follower = $("<div class=\"well well-sm\"><div class=\"pull-left align-middle\"><b>" + this['screenName'] + "</b></div></div>");

                    var deleteButton = $("<button type=\"button\" class=\"btn btn-danger\">Delete</button>");
                    $(deleteButton).data('index', index);
                    $(deleteButton).on( "click", function() {
                		editTwitterFollower($(this).data("index"), true);
					});

					var disableButton=$("<button type=\"button\" class=\"btn btn-primary" + (this['isEnabled'] ? "" : " btn-success") + "\">" + (this['isEnabled'] ? "Disable" : "Enable") + "</button>");
					$(disableButton).data('index', index);
                    $(disableButton).on( "click", function() {
                		editTwitterFollower($(this).data("index"), false);
					});

                    var buttonPanel = $("<div class=\"pull-right align-middle\"></div>");
                    buttonPanel.append(disableButton);
                    buttonPanel.append("&nbsp;&nbsp;")
                    buttonPanel.append(deleteButton);
                    follower.append(buttonPanel);

                    var clearFix = $("<div class=\"clearfix\"></div>");
                    follower.append(clearFix);

                    $("#followed").append(follower);
                });

                // Reddit settings
                $("#redditClientId").val(settings.reddit.redditClientId)
                $("#redditClientSecret").val(settings.reddit.redditClientSecret)
                $("#redditRefreshToken").val(settings.reddit.redditRefreshToken)
            }
        }).fail(function() {
    	    $('#infoModalContent').empty()
			$('#infoModalContent').append('Error connecting to RoliPrinter. Try again!');
			$('#infoModal').modal('show');
  	    });
  	}

  	function refreshLog() {
  	    $.ajax({
            type: "GET",
            url: "/api/systemLog",
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                log = JSON.parse(data)

                $("#systemLog").val(log.log);
            }
        }).fail(function() {
    	    $('#infoModalContent').empty()
			$('#infoModalContent').append('Error getting log');
			$('#infoModal').modal('show');
  	    });
  	}

  	function printNote(note, qrData) {
  		$.ajax({
			type: "POST",
			url: "/api/note",
			data: JSON.stringify({"note" : note, "qrData" : qrData}),
			contentType: "application/json",
			dataType: "json",
			success: function (data) {
				console.log("Note posted");
				$('#note').val('');
				$('#noteQrData').val('');

    			$('#notePrint').prop('disabled', false);
				refreshDisplay();
			}
		}).fail(function(jqXHR, textStatus, errorThrown) {
			$('#notePrint').prop('disabled', false);

			$('#infoModalContent').empty()
			$('#infoModalContent').append('Error printing a note. Have you actually entered any text?');
			$('#infoModal').modal('show');
		});
  	}

  	function saveRedditSettings(clientId, clientSecret, refreshToken) {
  		$.ajax({
			type: "POST",
			url: "/api/redditSaveSettings",
			data: JSON.stringify({"redditClientId" : clientId, "redditClientSecret" : clientSecret, "redditRefreshToken" : refreshToken}),
			contentType: "application/json",
			dataType: "json",
			success: function (data) {
				console.log("Reddit settings saved");

    			$('#redditSettingsSave').prop('disabled', false);
				refreshDisplay();
			}
		}).fail(function(jqXHR, textStatus, errorThrown) {
			$('#redditSettingsSave').prop('disabled', false);

			$('#infoModalContent').empty()
			$('#infoModalContent').append('Error saving reddit settings. Try again.');
			$('#infoModal').modal('show');
		});
  	}

  	function getRedditAuthorizationURL() {
  	    $.ajax({
            type: "GET",
            url: "/api/redditGetAuthorization",
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                auth = JSON.parse(data)

                $("#redditAuthorizationURL").val(auth.authURL);
                $('#redditAuthorizeAccount').prop('disabled', false);
                $("#createAuthorization").removeClass('hidden');
            }
        }).fail(function() {
            $('#redditAuthorizeAccount').prop('disabled', false);
            $("#createAuthorization").addClass('hidden');

    	    $('#infoModalContent').empty()
			$('#infoModalContent').append('Error getting reddit authorization URL. Missing client Id or client secret?');
			$('#infoModal').modal('show');
  	    });
  	}

  	function getRedditRefreshToken(code) {
  		$.ajax({
			type: "POST",
			url: "/api/redditGetRefreshToken",
			data: JSON.stringify({"code" : code}),
			contentType: "application/json",
			dataType: "json",
			success: function (data) {
				console.log("Reddit refresh token saved");

    			$('#redditRequestToken').prop('disabled', false);
    			$("#createAuthorization").addClass('hidden');
				refreshDisplay();
			}
		}).fail(function(jqXHR, textStatus, errorThrown) {
			$('#redditRequestToken').prop('disabled', false);

			$('#infoModalContent').empty()
			$('#infoModalContent').append('Error getting reddit refresh token. Try again.');
			$('#infoModal').modal('show');
		});
  	}

  	function saveGlobalSettings(usbPID, usbVID) {
  		$.ajax({
			type: "POST",
			url: "/api/settings",
			data: JSON.stringify({"usbPID" : usbPID, "usbVID" : usbVID}),
			contentType: "application/json",
			dataType: "json",
			success: function (data) {
				console.log("Global settings saved");

    			$('#globalSettingsSave').prop('disabled', false);
				refreshDisplay();
			}
		}).fail(function(jqXHR, textStatus, errorThrown) {
			$('#globalSettingsSave').prop('disabled', false);

			$('#infoModalContent').empty()
			$('#infoModalContent').append('Error saving global settings. Try again.');
			$('#infoModal').modal('show');
		});
  	}

  	refreshDisplay();
  	refreshLog();

  	setInterval(function() {
      refreshLog();
	}, 5000);

});
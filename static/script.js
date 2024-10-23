
$(document).ready(function() {
    let startDateSelected = false;

    // Show the filter modal on icon click
    $('#filter-icon').on('click', function() {
        $('#filterModal').show();
    });

    // Handle closing the modal
    $('.close-button').on('click', function() {
        $('#filterModal').hide();
    });

    // Automatically set start date and end date behavior
    $('#start-date').on('change', function() {
        if (!startDateSelected) {
            startDateSelected = true;
            $('#end-date').focus(); // Focus on the end date after selecting start date
        }
    });

    // Handle filter form submission
    $('#filter-form').on('submit', function(e) {
        e.preventDefault();
        var startDate = $('#start-date').val();
        var endDate = $('#end-date').val();
        var query = $('#search-query').val();

        // Ensure both dates are selected
        if (startDate && endDate) {
            // Make an AJAX request with the search query and selected dates
            $.get('/search_articles', { query: query, start: startDate, end: endDate }, function(data) {
                // Clear any previous search results
                $('#search-results-body').empty();

                // Check if there are any results
                if (data.length === 0) {
                    $('#search-results-body').append('<tr><td colspan="6">No matching articles found</td></tr>');
                } else {
                    // Populate the search results in the table
                    data.forEach(function(article) {
                        $('#search-results-body').append(
                            `<tr>
                                <td>${article.code_article}</td>
                                <td>${article.libelle_article}</td>
                                <td>${article.prix_achat}</td>
                                <td>${article.emplacement}</td>
                                <td>${article.quantite}</td>
                                <td>${article.fournisseur}</td>
                            </tr>`
                        );
                    });
                }

                // Close the modal after applying filters
                $('#filterModal').hide();
            });
        } else {
            alert("Please select both a start and end date.");
        }
    });

    // Handle the search form submission (without date filter)
    $('#search-form').on('submit', function(e) {
        e.preventDefault();
        var query = $('#search-query').val();

        // Make an AJAX request to the search route
        $.get('/search_articles', { query: query }, function(data) {
            // Clear any previous search results
            $('#search-results-body').empty();

            // Check if there are any results
            if (data.length === 0) {
                $('#search-results-body').append('<tr><td colspan="6">No matching articles found</td></tr>');
            } else {
                // Populate the search results in the table
                data.forEach(function(article) {
                    $('#search-results-body').append(
                        `<tr>
                            <td>${article.code_article}</td>
                            <td>${article.libelle_article}</td>
                            <td>${article.prix_achat}</td>
                            <td>${article.emplacement}</td>
                            <td>${article.quantite}</td>
                            <td>${article.fournisseur}</td>
                        </tr>`
                    );
                });
            }

            // Show the modal with search results
            $('#searchModal').show();
        });
    });
});




    $(document).ready(function() {
        // Show modal with animation
        $('#searchModal').addClass('show');

        // Handle the search form submission
        $('#search-form').on('submit', function(e) {
            e.preventDefault();  // Prevent default form submission

            // Get the search query from the input field
            var query = $('#search-query').val();

            // Make an AJAX request to the search route
            $.get('/search_articles', { query: query }, function(data) {
                $('#search-results-body').empty();  // Clear previous results

                if (data.length === 0) {
                    $('#search-results-body').append('<tr><td colspan="6">No matching articles found</td></tr>');
                } else {
                    data.forEach(function(article) {
                        $('#search-results-body').append(`
                            <tr>
                                <td>${article.code_article}</td>
                                <td>${article.libelle_article}</td>
                                <td>${article.prix_achat}</td>
                                <td>${article.emplacement}</td>
                                <td>${article.quantite}</td>
                                <td>${article.fournisseur}</td>
                            </tr>
                        `);
                    });
                }
                $('#searchModal').addClass('show');
            });
        });

        // Close modal on close-button click
        $('.close-button').on('click', function() {
            $('#searchModal').removeClass('show');
            $('#filterModal').hide();
        });

        // Open filter modal on filter icon click
        $('#filter-icon').on('click', function() {
            $('#filterModal').show();
        });
    });



$(document).ready(function() {
    $('#orders-list-item').on('click', function() {
        $.get('/pending_buys', function(data) {
            console.log("AJAX Response:", data);  // Log the response data
            $('#orders-body').empty();  // Clear previous entries
            
            // Check if data is empty
            if (data.length === 0) {
                $('#orders-body').append('<tr><td colspan="7">No pending orders found</td></tr>');
            } else {
                data.forEach(function(order) {
                    $('#orders-body').append(
                        `<tr>
                            <td>${order.code_demande}</td>
                            <td>${order.code_article}</td>
                            <td>${order.libelle_article}</td>
                            <td>${order.quantite}</td>
                            <td>${order.emplacement}</td>
                            <td>${new Date(order.date).toLocaleString()}</td>
                            <td>${order.demandeur}</td>
                        </tr>`
                    );
                });
            }
            $('#ordersModal').show();  // Show the modal
        }).fail(function(xhr, status, error) {
            console.error("AJAX Error:", status, error);  // Log any AJAX errors
        });
    });

    $('.close-button').on('click', function() {
        $('#ordersModal').hide();  // Hide the modal
    });
});


$(document).ready(function() {
    $('#total-sales-item').on('click', function() {
        $.get('/pending_sales', function(data) {  // Appel AJAX pour récupérer les demandes de vente
            console.log("AJAX Response:", data);  // Log the response data
            $('#sales-body').empty();  // Clear previous entries
            
            // Check if data is empty
            if (data.length === 0) {
                $('#sales-body').append('<tr><td colspan="7">No pending sales found</td></tr>');
            } else {
                data.forEach(function(sale) {
                    $('#sales-body').append(
                        `<tr>
                            
                            <td>${sale.code_article}</td>
                            <td>${sale.libelle_article}</td>
                            <td>${sale.quantite}</td>
                            <td>${sale.emplacement}</td>
                            <td>${new Date(sale.date).toLocaleString()}</td>
                            <td>${sale.demandeur}</td>
                        </tr>`
                    );
                });
            }
            $('#salesModal').show();  // Show the modal
        }).fail(function(xhr, status, error) {
            console.error("AJAX Error:", status, error);  // Log any AJAX errors
        });
    });

    $('.close-button').on('click', function() {
        $('#salesModal').hide();  // Hide the modal
    });
});



$(document).ready(function() {
    // Fetch recent orders when the page loads
    function fetchRecentOrders() {
        $.get('/recent_orders', function(data) {
            let ordersBody = $('#recent-orders-body');
            ordersBody.empty();  // Clear any previous entries

            // Loop through the orders and append rows to the table
            data.forEach(function(order) {
                ordersBody.append(`
                    <tr>
                        <td style="background-color: #e3ee8b; text-align:center;">${order.id_article}</td>
                        <td style="background-color: #dbe4fe; text-align:center;">${order.code_article}</td>
                        <td style="background-color: #b7df90; text-align:center;">${order.libelle_article}</td>  <!-- Display libelle article -->
                        <td style="background-color: #d6c1c4;text-align:center;">${order.date_order}</td>
                        <td style="background-color: #cea8b1;text-align:center;">${order.emplacement}</td>
                        <td style="background-color: #d7dfa5;text-align:center;">${order.quantite}</td>
                    </tr>
                `);
            });
        }).fail(function(xhr, status, error) {
            console.error("Error fetching recent orders:", status, error);
        });
    }

    // Call the function to fetch and display recent orders
    fetchRecentOrders();
});



const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item=> {
	const li = item.parentElement;

	item.addEventListener('click', function () {
		allSideMenu.forEach(i=> {
			i.parentElement.classList.remove('active');
		})
		li.classList.add('active');
	})
});





const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
})







const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
	if(window.innerWidth < 576) {
		e.preventDefault();
		searchForm.classList.toggle('show');
		if(searchForm.classList.contains('show')) {
			searchButtonIcon.classList.replace('bx-search', 'bx-x');
		} else {
			searchButtonIcon.classList.replace('bx-x', 'bx-search');
		}
	}
})





if(window.innerWidth < 768) {
	sidebar.classList.add('hide');
} else if(window.innerWidth > 576) {
	searchButtonIcon.classList.replace('bx-x', 'bx-search');
	searchForm.classList.remove('show');
}


window.addEventListener('resize', function () {
	if(this.innerWidth > 576) {
		searchButtonIcon.classList.replace('bx-x', 'bx-search');
		searchForm.classList.remove('show');
	}
})



const switchMode = document.getElementById('switch-mode');

switchMode.addEventListener('change', function () {
	if(this.checked) {
		document.body.classList.add('dark');
	} else {
		document.body.classList.remove('dark');
	}
})


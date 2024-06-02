document.addEventListener('DOMContentLoaded', () => {
    const filmsPerPage = 10; // Number of films to display per page
    let currentPage = 1; // Initially displayed page

    // Function to render films on the table
    const renderFilms = (films) => {
        const startIndex = (currentPage - 1) * filmsPerPage;
        const endIndex = startIndex + filmsPerPage;
        const paginatedFilms = films.slice(startIndex, endIndex);

        const tableBody = document.getElementById('filmTableBody');
        tableBody.innerHTML = ''; // Clear the table

        paginatedFilms.forEach(film => {
            const row = document.createElement('tr');

            // Create the cast list
            const castList = film["Cast List"].slice(0, 5).map(cast => 
                `<a href="https://letterboxd.com${cast.castActorpage}" target="_blank">${cast.castRealName}</a> as ${cast.character}`
            ).join(', ');

            row.innerHTML = `
                <td><a href="${film.movie_url}" target="_blank">${film.movieName}</a></td>
                <td>${film.directorName}</td>
                <td>${film.releaseYear}</td>
                <td>${film.info}</td>
                <td>${film.rating}</td>
                <td>${castList}</td>
                <td>${film.top250_rank}</td>
                <td>${film.watches}</td>
                <td>${film.likes}</td>
            `;
            tableBody.appendChild(row);
        });
    };

    // Function to fetch and render films
    const fetchAndRenderFilms = () => {
        fetch('films.json')
            .then(response => response.json())
            .then(films => {
                const sortedFilms = sortByRank(films);
                renderFilms(sortedFilms);
                renderPagination(sortedFilms.length);
            })
            .catch(error => console.error('Error loading the film data:', error));
    };

    // Function to render pagination buttons
    const renderPagination = (totalFilms) => {
        const totalPages = Math.ceil(totalFilms / filmsPerPage);
        const paginationContainer = document.getElementById('pagination');

        paginationContainer.innerHTML = ''; // Clear the pagination buttons

        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.innerText = i;
            pageButton.classList.add('page-link');
            if (i === currentPage) {
                pageButton.classList.add('active');
            }
            pageButton.addEventListener('click', () => {
                currentPage = i;
                fetchAndRenderFilms();
            });
            paginationContainer.appendChild(pageButton);
        }
    };

    // Function to sort films by rank
    const sortByRank = (films) => {
        return films.sort((a, b) => a.top250_rank - b.top250_rank);
    };

    // Initial call to fetch and render films
    fetchAndRenderFilms();
});

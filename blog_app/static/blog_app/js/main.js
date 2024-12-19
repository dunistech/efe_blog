

// Array of categories to rotate
const categories = ["Frontend Development", "Backend Development", "Full Stack Development", "Cyber Security", "Data Analysis"];

let currentCategoryIndex = 0;

function animateCategory() {
    const categoryElement = document.getElementById('animated-category');
    categoryElement.textContent = categories[currentCategoryIndex];

    // Increment the index, reset if out of bounds
    currentCategoryIndex = (currentCategoryIndex + 1) % categories.length;

    // Add fade-in effect
    categoryElement.style.opacity = '0';
    setTimeout(() => {
        categoryElement.style.opacity = '1';
    }, 200);
}

// Change category every 2 seconds
setInterval(animateCategory, 2000);



// modal overlay To View Post Image and Video
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("media-modal");
    const modalImage = document.getElementById("modal-image");
    const modalVideo = document.getElementById("modal-video");
    const modalVideoSource = document.getElementById("modal-video-source");
    const closeModal = document.querySelector(".close-modal");

    // Attach click event to media thumbnails
    document.querySelectorAll(".media-thumbnail").forEach((media) => {
        media.addEventListener("click", function () {
            modal.style.display = "flex"; // Show modal
            if (media.tagName.toLowerCase() === "img") {
                modalImage.style.display = "block";
                modalImage.src = media.src;
                modalVideo.style.display = "none";
            } else if (media.tagName.toLowerCase() === "video") {
                modalVideo.style.display = "block";
                modalVideoSource.src = media.querySelector("source").src;
                modalVideo.load(); // Ensure video is loaded
                modalImage.style.display = "none";
            }
        });
    });

    // Close modal when close button is clicked
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Close modal when clicking outside the content
    modal.addEventListener("click", function (e) {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
});





/*_______________________________________________________________________
    Function That Handle Read More and Show Less Text truncate 
_______________________________________________________________________*/
function toggleReadMore() {
    const contentContainers = document.querySelectorAll('.post-content-container');

    contentContainers.forEach((container) => {
        const content = container.getAttribute('data-full-content').trim();
        const readMoreBtn = container.nextElementSibling;

        // Threshold length for truncation
        const maxLength = 35;

        if (content.length > maxLength) {
            // Truncate content and add ellipsis
            const truncatedContent = content.slice(0, maxLength) + '...';
            container.querySelector('.post-content').textContent = truncatedContent;

            // Show the "Read More" button
            readMoreBtn.style.display = 'inline-block';

            // Add click event to toggle full content
            readMoreBtn.addEventListener('click', () => {
                if (container.classList.contains('expanded')) {
                    container.classList.remove('expanded');
                    container.querySelector('.post-content').textContent = truncatedContent;
                    readMoreBtn.textContent = 'Read More...';
                } else {
                    container.classList.add('expanded');
                    container.querySelector('.post-content').textContent = content;
                    readMoreBtn.textContent = 'Show Less';
                }
            });
        }
    });
}

// Wait for the DOM content to be loaded before running the function
document.addEventListener('DOMContentLoaded', toggleReadMore);




// document.addEventListener('DOMContentLoaded', () => {
//     const contentContainers = document.querySelectorAll('.post-content-container');

//     contentContainers.forEach((container) => {
//         const content = container.getAttribute('data-full-content').trim();
//         const readMoreBtn = container.nextElementSibling;

//         // Threshold length for truncation
//         const maxLength = 35;

//         if (content.length > maxLength) {
//             // Truncate content and add ellipsis
//             const truncatedContent = content.slice(0, maxLength) + '...';
//             container.querySelector('.post-content').textContent = truncatedContent;

//             // Show the "Read More" button
//             readMoreBtn.style.display = 'inline-block';

//             // Add click event to toggle full content
//             readMoreBtn.addEventListener('click', () => {
//                 if (container.classList.contains('expanded')) {
//                     container.classList.remove('expanded');
//                     container.querySelector('.post-content').textContent = truncatedContent;
//                     readMoreBtn.textContent = 'Read More...';
//                 } else {
//                     container.classList.add('expanded');
//                     container.querySelector('.post-content').textContent = content;
//                     readMoreBtn.textContent = 'Show Less';
//                 }
//             });
//         }
//     });
// });





/*_______________________________________________________________________
    // Scroll Recent Paginated Post 
_______________________________________________________________________*/
function scrollRecentPaginatedPost() {
    // When the page loads, check for a hash in the URL
    window.onload = function () {
        // Check if there's a hash in the URL (post ID)
        const hash = window.location.hash;
        if (hash) {
            // Get the post ID from the hash (e.g., #post-123)
            const postId = hash.substring(1);
            const targetElement = document.getElementById(postId);

            // Scroll to the post if it exists
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    };

    // Listen for clicks on the recent post links
    document.querySelectorAll('.recent-post-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent default anchor behavior

            // Get the page number and post ID from the href attribute
            const href = this.getAttribute('href');
            const urlParams = new URLSearchParams(href.split('?')[1]);
            const page = urlParams.get('page'); // Get the page number
            const postId = href.split('#')[1]; // Get the post ID from the hash

            // Redirect to the correct page with the post ID in the URL
            window.location.href = `${href}`;

            // Wait for the page to load, then scroll to the post
            window.onload = function () {
                const targetElement = document.getElementById(postId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            };
        });
    });
}
// Wait for the DOM content to be loaded before running the function
document.addEventListener('DOMContentLoaded', scrollRecentPaginatedPost);


// <!-- Update Post Action Icon Button -->
function toggleCustomDropdown(button) {
    const dropdownMenu = button.nextElementSibling;
    dropdownMenu.classList.toggle('show-custom-dropdown');
}

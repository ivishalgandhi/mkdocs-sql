document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.sql-wrapper').forEach(function(wrapper, index) {
        // Handle SQL query toggle
        const sqlBlock = wrapper.querySelector('.sql-query');
        const sqlToggle = wrapper.querySelector('.sql-toggle');
        const sqlIcon = sqlToggle.querySelector('.material-icons');
        
        // Set initial state based on localStorage or default to hidden
        const isQueryVisible = localStorage.getItem(`sql-visible-${index}`) === 'true';
        sqlBlock.style.display = isQueryVisible ? 'block' : 'none';
        sqlToggle.classList.toggle('active', isQueryVisible);
        
        // Add click handler for SQL toggle
        sqlToggle.addEventListener('click', function() {
            const isCurrentlyVisible = sqlBlock.style.display === 'block';
            sqlBlock.style.display = isCurrentlyVisible ? 'none' : 'block';
            sqlToggle.classList.toggle('active');
            localStorage.setItem(`sql-visible-${index}`, !isCurrentlyVisible);
        });

        // Handle table view toggle
        const tableToggle = wrapper.querySelector('.table-toggle');
        if (tableToggle) {
            const formattedTable = wrapper.querySelector('.formatted-table');
            const rawTable = wrapper.querySelector('.raw-table');
            const tableIcon = tableToggle.querySelector('.material-icons');
            
            // Always start with formatted table view
            formattedTable.style.display = 'block';
            rawTable.style.display = 'none';
            tableIcon.textContent = 'grid_on';
            tableToggle.classList.remove('active');
            
            // Add click handler for table toggle
            tableToggle.addEventListener('click', function() {
                const isCurrentlyRaw = formattedTable.style.display === 'none';
                formattedTable.style.display = isCurrentlyRaw ? 'block' : 'none';
                rawTable.style.display = isCurrentlyRaw ? 'none' : 'block';
                tableIcon.textContent = isCurrentlyRaw ? 'grid_on' : 'table_rows';
                tableToggle.classList.toggle('active');
            });
        }
    });
});

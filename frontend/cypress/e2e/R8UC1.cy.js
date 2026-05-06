describe('Use case R8UC1', () => {
    let uid;
    let name;
    let email;
    let videos;

    before(() => {
        cy.fixture('user.json').then((user) => {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/users/create',
                form: true,
                body: user
            }).then((response) => {
                uid = response.body._id.$oid;
                email = user.email;
            }).then(() => {
                cy.visit('http://localhost:3000');
                cy.get('#email').type(email);
                cy.get('form').submit();
                cy.get('#title').type('Test Task');
                cy.get('.submit-form').submit();
                cy.contains('Test Task').click();
            });
        });
    });


    after(() => {
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`,
        }).then((response) => {
            expect(response.body.success).to.be.true;
        });
    });

    it('The user enters a description of a todo item and creates it', () => {
        cy.get('.inline-form > [type="text"]').type('todo test');
        cy.get('.inline-form > [type="submit"]').click();

        cy.contains('todo test').should('exist');
    });

    it('Test if the new (active) todo item is appended to the bottom of the list of existing todo items', () => {
        cy.get('.todo-list .todo-item').last().should('contain', 'todo test');
    });


    it('If the description is empty then the “Add” button should remain disabled', () => {
        cy.get('.inline-form > [type="text"]').clear();
        cy.get('.inline-form > [type="submit"]').should('be.disabled');
    });
});


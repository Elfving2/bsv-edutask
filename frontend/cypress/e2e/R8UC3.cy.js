describe('Use case R8UC3', () => {
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

                // Create a new todo item
                cy.get('.inline-form > [type="text"]').type('todo test delete item');
                cy.get('.inline-form > [type="submit"]').click();
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

    it('When pressing the x symbol behind the description, todo item should be deleted', () => {
        cy.contains('.todo-item', 'todo test delete item').as('todoTestDeleteItem');

        cy.get('@todoTestDeleteItem')
            .find('span.remover').click();

        cy.contains('@todoTestDeleteItem').should('not.exist');

    });
});

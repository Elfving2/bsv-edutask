let email;
let uid;
describe('Use cases R8UC1, R8UC2, R8UC3', () => {
    beforeEach(() => {
        cy.fixture('user.json').then((user) => {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/users/create',
                form: true,
                body: user
            }).then((response) => {
                email = user.email;
                uid = response.body._id.$oid;
                cy.fixture('task.json').then((task) => {
                    cy.request({
                        method: 'POST',
                        url: 'http://localhost:5000/tasks/create',
                        form: true,
                        body: {
                            title: task.title,
                            description: task.description,
                            url: task.url,
                            userid: uid,
                            todos: task.todos[0]
                        }
                    }).then((response) => {
                        cy.visit('http://localhost:3000');
                        cy.get('#email').type(email);
                        cy.get('form').submit();

                        cy.contains(task.title).click();
                    });
                });
            });

        });
    });

    afterEach(() => {
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`,
        }).then((response) => {
            expect(response.body.success).to.be.true;
        });
    });

    it('If the description is empty then the “Add” button should remain disabled', () => {
        cy.get('.inline-form > [type="text"]').clear();

        cy.get('.inline-form > [type="submit"]')
            .should('be.disabled')
    })

    it('If the description is not empty and the user presses “Add”, the system creates a new todo item', () => {
        cy.get('.inline-form > [type="text"]').type('Test Todo');
        cy.get('.inline-form > [type="submit"]').click();

        cy.get('.todo-list').children('.todo-item').last().should('contain.text', 'Test Todo');

    })

    it('marks an active todo as done and crosses out its text', () => {
        cy.contains('.todo-item', 'Test Todo').as('todoitem');

        cy.get('@todoitem').find('span.checker').click()

        cy.get('@todoitem').find('span.checker').should('have.class', 'checked')

        cy.get('@todoitem').find('span.editable').should('have.css', 'text-decoration-line', 'line-through')
    })

    it('mark an done todo as active and text should no longer be crossed out', () => {
        cy.contains('.todo-item', 'Test Todo').as('todoitem');

        cy.get('@todoitem').find('span.checker').click()

        cy.get('@todoitem').find('span.checker').should('have.class', 'checked')

        cy.get('@todoitem').find('span.checker').click()

        cy.get('@todoitem').find('span.checker').should('have.class', 'unchecked')

        cy.get('.todo-list .todo-item .editable').should('not.have.css', 'text-decoration-line', 'line-through')
    })

    it('deletes a todo item and removes it from the list', () => {
        cy.contains('.todo-item', 'Test Todo').find('span.remover').click();
        cy.contains('.todo-item', 'Test Todo').should('not.exist');

    });
});
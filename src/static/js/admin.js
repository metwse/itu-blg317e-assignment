class XTable extends HTMLElement {
  constructor() {
    super();

    this._mode = 'get';
    this._fields = {};
    this._keys = [];
  }

  connectedCallback() {
    const observer = new MutationObserver(() => {
      observer.disconnect();

      this.classList.add('get');

      const query = document.createElement('div');
      query.className = 'query';

      const result = document.createElement('pre');

      const fields = document.createElement('div');
      fields.className = 'fields';

      for (const child of [...this.children]) {
        this.removeChild(child);

        const field = document.createElement('div');
        field.classList.add('field');

        field.appendChild(child);

        if (child.tagName == 'INPUT') {
          child.placeholder = child.name.replaceAll('_', ' ');
          if (child.type == 'checkbox') {
            const label = document.createElement('label');
            label.for = child.id = Math.random();
            label.innerText = child.placeholder;

            field.classList.add('checkbox');

            field.insertBefore(label, child);
          }
        }

        const constraints = document.createElement('div');
        constraints.className = 'constraints';

        if (child.hasAttribute('x-key')) {
          constraints.innerHTML += '<span class="key">key</span>';
          this._keys.push(child.name);
        }
        if (child.hasAttribute('x-nocreate'))
          constraints.innerHTML += '<span class="serial">serial</span>';
        if (child.hasAttribute('x-opt'))
          constraints.innerHTML += '<span class="optional">optional</span>';

        if (constraints.innerHTML)
          field.appendChild(constraints);

        this._fields[child.name] = child;

        fields.appendChild(field);
      };

      query.appendChild(fields);
      query.appendChild(result);

      this._result = result;

      const h2 = document.createElement('h2');
      h2.innerHTML = this.getAttribute('x-table').replaceAll('_', ' ');
      this.appendChild(h2);

      this.appendChild(query);

      const control = document.createElement('div');
      control.className = 'control';
      control.innerHTML = `
        <button class="list-all">list all items</button>
        <div class="mode">
          <span>MODE</span>
          <div>
            <button disabled>get</button>
            <button>delete</button>
            <button>create</button>
            <button>update</button>
          </div>
          <button class="send">send</button>
        </div>
      `;

      const modeButtons = control.querySelectorAll('.mode > div > button');
      for (const button of modeButtons) {
        button.onclick = () => {
          modeButtons.forEach(b => b.removeAttribute('disabled'));

          this.classList.remove(this._mode);
          this._mode = button.innerText;
          this.classList.add(this._mode);

          button.setAttribute('disabled', 1);
        };
      }

      control.querySelector('.send').onclick = () => this._send();
      control.querySelector('.list-all').onclick = () => this._list_all();

      this.appendChild(control);
    });

    observer.observe(this, { childList: true, subtree: true });
  }

  async _list_all() {
    this._result.innerText = '...';

    const res = await fetch(
      `/internal/${this.getAttribute('x-table')}/`,
      {
        headers: {
          'Content-Type': 'application/json',
          'Token': document.getElementById('token').value,
        },
        method: 'GET',
      }
    ).then(r => r.json());

    this._result.innerText = JSON.stringify(res, null, 2);
  }

  async _send() {
    const fields = {};

    for (const [k, v] of Object.entries(this._fields)) {
      fields[k] = v.value;

      if (v.type == 'number')
        fields[k] = +(fields[k] || 0);

      if (v.type == 'checkbox')
        fields[k] = v.checked;

      if (v.hasAttribute('x-opt') && v.value == '')
          fields[k] = null;
    }

    this._result.innerText = '...';

    const url = this._mode == 'create' ? '' :
      this._keys.map(key => `${fields[key]}`).join('/');

    const res = await fetch(
      `/internal/${this.getAttribute('x-table')}/${url}`,
      {
        headers: {
          'Content-Type': 'application/json',
          'Token': document.getElementById('token').value,
        },
        method: {
          get: 'GET',
          delete: 'DELETE',
          update: 'PATCH',
          create: 'POST'
        }[this._mode],
        body: this._mode == 'get' ? undefined : JSON.stringify(fields),
      }
    ).then(r => r.json());

    this._result.innerText = JSON.stringify(res, null, 2);
  }
}

customElements.define('x-table', XTable);

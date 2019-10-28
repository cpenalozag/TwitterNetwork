import React, {Component} from "react";

class About extends Component {
    constructor(props) {
        super(props);

        this.handleInputChange = this.handleInputChange.bind(this);
    }

    handleInputChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        const parts = name.split(",")
        const type = parts[0]
        const material = parts[1]
        const period = parts[2]

        try {
            const v = parseFloat(value)
            if (v >= 0) {
                Meteor.call("materials.updateCost", type, material, period, value)
            }
        } catch (e) {

        }
    }

    renderCostsLeadTime() {
        return this.props.materials.map((material) => {
            return (
                <tr key={material._id}>
                    <td className="first-row">{material.nombre}</td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`ordenar,${material.nombre},menos2`} min="0" required="" type="number"
                               defaultValue={material.costos.ordenar.menos2}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`adquirir,${material.nombre},menos2`} min="0" required="" type="number"
                               defaultValue={material.costos.adquirir.menos2}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`mantener,${material.nombre},menos2`} min="0" required="" type="number"
                               defaultValue={material.costos.mantener.menos2}/></td>

                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`ordenar,${material.nombre},menos1`} min="0" required="" type="number"
                               defaultValue={material.costos.ordenar.menos1}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`adquirir,${material.nombre},menos1`} min="0" required="" type="number"
                               defaultValue={material.costos.adquirir.menos1}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`mantener,${material.nombre},menos1`} min="0" required="" type="number"
                               defaultValue={material.costos.mantener.menos1}/></td>

                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`ordenar,${material.nombre},cero`} min="0" required="" type="number"
                               defaultValue={material.costos.ordenar.cero}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`adquirir,${material.nombre},cero`} min="0" required="" type="number"
                               defaultValue={material.costos.adquirir.cero}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`mantener,${material.nombre},cero`} min="0" required="" type="number"
                               defaultValue={material.costos.mantener.cero}/></td>
                </tr>
            )
        });
    }

    renderCostsFirst() {
        return this.props.materials.map((material) => {
            return (
                <tr key={material._id}>
                    <td className="first-row">{material.nombre}</td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`ordenar,${material.nombre},primero`} min="0" required="" type="number"
                               defaultValue={material.costos.ordenar.primero}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`adquirir,${material.nombre},primero`} min="0" required="" type="number"
                               defaultValue={material.costos.adquirir.primero}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`mantener,${material.nombre},primero`} min="0" required="" type="number"
                               defaultValue={material.costos.mantener.primero}/></td>

                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`ordenar,${material.nombre},segundo`} min="0" required="" type="number"
                               defaultValue={material.costos.ordenar.segundo}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`adquirir,${material.nombre},segundo`} min="0" required="" type="number"
                               defaultValue={material.costos.adquirir.segundo}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`mantener,${material.nombre},segundo`} min="0" required="" type="number"
                               defaultValue={material.costos.mantener.segundo}/></td>

                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`ordenar,${material.nombre},tercero`} min="0" required="" type="number"
                               defaultValue={material.costos.ordenar.tercero}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`adquirir,${material.nombre},tercero`} min="0" required="" type="number"
                               defaultValue={material.costos.adquirir.tercero}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`mantener,${material.nombre},tercero`} min="0" required="" type="number"
                               defaultValue={material.costos.mantener.tercero}/></td>
                </tr>
            )
        });
    }

    renderCostsSecond() {
        return this.props.materials.map((material) => {
            return (
                <tr key={material._id}>
                    <td className="first-row">{material.nombre}</td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`ordenar,${material.nombre},cuarto`} min="0" required="" type="number"
                               defaultValue={material.costos.ordenar.cuarto}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`adquirir,${material.nombre},cuarto`} min="0" required="" type="number"
                               defaultValue={material.costos.adquirir.cuarto}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`mantener,${material.nombre},cuarto`} min="0" required="" type="number"
                               defaultValue={material.costos.mantener.cuarto}/></td>

                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`ordenar,${material.nombre},quinto`} min="0" required="" type="number"
                               defaultValue={material.costos.ordenar.quinto}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`adquirir,${material.nombre},quinto`} min="0" required="" type="number"
                               defaultValue={material.costos.adquirir.quinto}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`mantener,${material.nombre},quinto`} min="0" required="" type="number"
                               defaultValue={material.costos.mantener.quinto}/></td>

                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`ordenar,${material.nombre},sexto`} min="0" required="" type="number"
                               defaultValue={material.costos.ordenar.sexto}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`adquirir,${material.nombre},sexto`} min="0" required="" type="number"
                               defaultValue={material.costos.adquirir.sexto}/></td>
                    <td><input className="form-control text-center" onChange={this.handleInputChange}
                               name={`mantener,${material.nombre},sexto`} min="0" required="" type="number"
                               defaultValue={material.costos.mantener.sexto}/></td>
                </tr>
            )
        });
    }

    render() {
        return (
            <div className="container-fluid">
                <div className="card">
                    <div className="content">
                        <div className="card-header ">
                            <h4 className="card-title">How to use the app</h4>
                        </div>
                        <div className="card-body ">
                            <p>This web application can help you find the twitter user/s that can obtain the greatest
                                engagement (likes + retweets) when publishing your message. The steps to use the app
                                are:</p>
                            <ol>
                                <li>Go to the search tab</li>
                                <li>Type the message you want to post</li>
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default About;